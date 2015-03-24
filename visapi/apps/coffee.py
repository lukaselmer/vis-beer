
import vislib.flags
import vislib.person
import webob.exc
import datetime
import logging
from sqlalchemy import sql, schema, create_engine
from visapi.rest.dec import restful
from visapi.rest import json, xml
import ConfigParser

beer_flag = 'beers'
coffee_flag = 'coffee'
datetime_fmt = "%Y-%m-%d %H:%M:%S"
logger = logging.getLogger("coffee")

def daybegin():
    cutoff = datetime.time(3, 0)
    if datetime.datetime.now().time() < cutoff:
        day = datetime.date.today() - datetime.timedelta(days=1)
    else:
        day = datetime.date.today()
    return datetime.datetime.combine(day, cutoff)

remaining_xmlser_fmt = "<remaining&.coffees>"
@restful(accept=json.accept() + xml.accept_xmlser(remaining_xmlser_fmt),
         methods=["GET"])
def remaining(req, args, make_response):
    lookup = args['lookup']
    try:
        person = vislib.person.get_person(lookup)
    except vislib.person.InvalidPerson as e:
        raise webob.exc.HTTPNotFound(str(e))

    config = None
    try:
        from visapi.utils import get_config
        config = get_config()
    except Exception:
        logger.error("exception while loading config", exc_info=True)

    values = vislib.flags.get_flag_values(coffee_flag, person.uniqueid)

    perday = int(values.get('perday') or 0)
    if 'perday' not in values and not person.vismember:
        raise webob.exc.HTTPNotFound()
    elif 'perday' not in values:
        try:
            if config.has_option('coffee', 'default_perday'):
                perday_ = config.get('coffee', 'default_perday')
                vislib.flags.set_flag_value(coffee_flag, person.uniqueid, 'perday', str(perday_))
                perday = perday_
        except Exception:
            logger.error("exception while getting default perday", exc_info=True)

    remaining = int(values.get('remaining') or perday)

    last = values.get('last') or None
    if last:
        last = datetime.datetime.strptime(last, datetime_fmt)
    if last and last < daybegin():
        remaining = perday
    if last and not values.get('nolimit') and config.has_option('coffee', 'rate_limit_minutes'):
        try:
            limit = config.getint('coffee', 'rate_limit_minutes')
        except Exception:
            logger.error("exception while reading rate limit from config")
        else:
            if last > datetime.datetime.now() - datetime.timedelta(minutes=limit):
                remaining = 0

    purchased = int(values.get('purchased') or 0)
    remaining += purchased

    # for every beer consumed today, remove 2 coffees
    remaining -= dispensed_beers_today(person) * 2
    remaining = max(remaining, 0)

    return make_response(req, dict(coffees=remaining))


def dispensed_beers_today(person):
    values = vislib.flags.get_flag_values(beer_flag, person.uniqueid)

    last = values.get('last') or None
    if last and datetime.datetime.strptime(last, datetime_fmt) < daybegin():
        # No coffee consume today
        return 0

    return int(values.get('dispensed_today') or 0)


@restful(methods=["POST"])
def dispensed(req, args, make_response):
    lookup = args['lookup']
    try:
        person = vislib.person.get_person(lookup)
    except vislib.person.InvalidPerson as e:
        raise webob.exc.HTTPNotFound(str(e))

    values = vislib.flags.get_flag_values("coffee", person.uniqueid)

    perday = int(values.get('perday') or 0)
    remaining = int(values.get('remaining') or perday)

    last = values.get('last')
    dispensed_today = int(values.get('dispensed_today') or 0)
    if last and datetime.datetime.strptime(last, datetime_fmt) < daybegin():
        remaining = perday
        dispensed_today = 0

    purchased = int(values.get('purchased') or 0)
    unexpected = int(values.get('unexpected') or 0)
    total = int(values.get('total') or 0)
    now = datetime.datetime.now().strftime(datetime_fmt)

    if remaining > 0:
        vislib.flags.set_flag_value(coffee_flag, person.uniqueid, 'remaining', remaining - 1)
    elif purchased > 0:
        vislib.flags.set_flag_value(coffee_flag, person.uniqueid, 'purchased', purchased - 1)
    else:
        vislib.flags.set_flag_value(coffee_flag, person.uniqueid, 'unexpected', unexpected + 1)
    vislib.flags.set_flag_value(coffee_flag, person.uniqueid, 'total', total + 1)
    vislib.flags.set_flag_value(coffee_flag, person.uniqueid, 'dispensed_today', dispensed_today + 1)

    vislib.flags.set_flag_value(coffee_flag, person.uniqueid, 'last', now)

    return make_response(req, '')

coffeelog_metadata = schema.MetaData()
coffeelog = coffeelog_dbengine = coffeelog_sql = coffeelog_sql_cut = coffeelog_perday = None
def coffeelog_connect():
    global coffeelog, coffeelog_dbengine, coffeelog_sql, coffeelog_sql_cut, coffeelog_perday

    if not coffeelog_dbengine:
        from visapi.utils import get_config
        config = get_config()
        db_uri = config.get('coffee', 'log_db_uri')
        dbengine = create_engine(db_uri, pool_recycle=3600)
        coffeelog = schema.Table('coffee', coffeelog_metadata, autoload=True, autoload_with=dbengine)
        coffeelog_sql = sql.select([
            coffeelog.c.msg,
            coffeelog.c.time,
        ]).where(
            coffeelog.c.type == sql.expression.bindparam('type')
        ).order_by(
            coffeelog.c.time.desc()
        )
        coffeelog_sql_cut = coffeelog_sql.where(
            coffeelog.c.time > sql.expression.bindparam('cutoff')
        )

        coffeelog_perday = sql.select([
            sql.func.count(coffeelog.c.id),
            sql.func.date(coffeelog.c.time)
        ]).where(sql.and_(
            coffeelog.c.type == 'DISPENSE',
            coffeelog.c.time > sql.expression.bindparam('cutoff')
        )).order_by(
            coffeelog.c.time.asc()
        ).group_by(
            sql.func.date(coffeelog.c.time)
        )

        coffeelog_dbengine = dbengine

    return coffeelog_dbengine

def query_type(dbengine, type, **delta_args):
    if delta_args:
        cutoff = datetime.datetime.now() - datetime.timedelta(**delta_args)
        return dbengine.execute(coffeelog_sql_cut, type=type, cutoff=cutoff)
    else:
        return dbengine.execute(coffeelog_sql, type=type)

stats_xmlser_fmt = "<stats<org*.orgs<name&.0><count&.1>><person*.rfids<rfid&.0><count&.1>><item*.items<itemnr&.0><count&.1>><day*.dates<date&.0><count&.1>>>"
@restful(accept=json.accept() + xml.accept_xmlser(stats_xmlser_fmt),
         methods=["GET"])
def stats(req, args, make_response):

    deltaargs = {}
    try:
        if 'days' in args:
            deltaargs.update(days=int(args['days']))
    except ValueError as e:
        raise webob.exc.HTTPBadRequest(str(e))

    rfid = None
    if 'lookup' in args:
        person = vislib.person.get_person(args['lookup'])
        if not person.rfid:
            return make_response(req, [])
        rfid = person.rfid
    elif 'rfid' in args:
        rfid = args['rfid']

    rows = query_type(coffeelog_connect(), 'DISPENSE', **deltaargs)

    def make_entry(row):
        try:
            values = row['msg'].split(':')
            return dict(org=values[0], rfid=values[1], item=values[2],
                        time=row['time'])
        except (IndexError, ValueError):
            pass
    entries = (make_entry(row) for row in rows)

    if rfid:
        entries = (e for e in entries if e['rfid'] == rfid)

    summary = dict(orgs={}, rfids={}, items={}, dates={})

    # values are wrapped in tuples so they can be incremented
    for e in entries:
        summary['orgs'].setdefault(e['org'], [0])[0] += 1
        summary['rfids'].setdefault(e['rfid'], [0])[0] += 1
        summary['items'].setdefault(e['item'], [0])[0] += 1
        summary['dates'].setdefault(str(e['time'].date()), [0])[0] += 1

    # now we strip the tuples away
    summary = dict(
        (k, dict((n, l[0]) for n, l in v.iteritems()))
        for k, v
        in summary.items()
    )

    return make_response(req, summary)

consumption_histogram_xmlser_fmt = "<histogram\
<total<bucket*.total<consumption&.consumption><count&.count>>>\
<organisation*.organisations<name&.0><bucket*.1\
<consumption&.consumption><count&.count>>>\
>"
@restful(accept=json.accept() + xml.accept_xmlser(consumption_histogram_xmlser_fmt),
         methods=["GET"])
def consumption_histogram(req, args, make_response):

    days = args['days']

    rows = query_type(coffeelog_connect(), 'DISPENSE', days=days)

    consumption = {}
    max_val = 0
    orgs = set()
    for row in rows:
        try:
            organisation, rfid, flavour = row['msg'].split(':')
        except (IndexError, ValueError):
            continue
        orgs.add(organisation)

        consumption.setdefault(rfid, {'organisation': organisation, 'count': 0})['count'] += 1
        if consumption[rfid]['count'] > max_val:
            max_val = consumption[rfid]['count']

    zeroed = dict((i, 0) for i in xrange(1, max_val + 1))
    histogram = dict(
        organisations=dict((o, zeroed.copy()) for o in orgs),
        total=zeroed.copy()
    )

    for item in consumption.values():
        histogram['organisations'][item['organisation']][item['count']] += 1
        histogram['total'][item['count']] += 1

    for org, item in histogram['organisations'].items():
        histogram['organisations'][org] = [dict(consumption=k, count=v) for k, v in item.iteritems()]
    histogram['total'] = [dict(consumption=k, count=v) for k, v in histogram['total'].iteritems()]

    return make_response(req, histogram)

consumption_perday_xmlser_fmt = "<consumption<day*?<date&.0><count&.1>>>"
@restful(accept=json.accept() + xml.accept_xmlser(consumption_perday_xmlser_fmt),
         methods=["GET"])
def consumption_perday(req, args, make_response):

    days = args['days']

    db_engine = coffeelog_connect()
    rows = db_engine.execute(coffeelog_perday, cutoff=datetime.datetime.now() - datetime.timedelta(days=days))

    today = datetime.date.today()

    res = dict(((today - datetime.timedelta(days=x)).isoformat(), 0) for x in xrange(0, days+1))

    for row in rows:
        res[row[1].isoformat()] = row[0]

    return make_response(req, res)

consumption_perday_detailed_xmlser_fmt = "<consumption\
<total<day*.total<date&.0><count&.1>>>\
<organisation*.organisation<name&.0><day*.1<date&.0><count&.1>>>\
<flavour*.flavour<name&.0><day*.1<date&.0><count&.1>>>\
>"
@restful(accept=json.accept() + xml.accept_xmlser(consumption_perday_detailed_xmlser_fmt),
         methods=["GET"])
def consumption_perday_detailed(req, args, make_response):
    days = args['days']

    rows = query_type(coffeelog_connect(), 'DISPENSE', days=days)

    today = datetime.date.today()

    # Initialize all days to 0
    zeroed = dict(((today - datetime.timedelta(days=x)).isoformat(), 0) for x in xrange(0, days+1))

    res = {
        'total': zeroed.copy(),
        'organisation': {},
        'flavour': {}
    }

    for row in rows:
        try:
            organisation, rfid, flavour = row['msg'].split(':')
        except (IndexError, ValueError):
            continue

        flavour = slot_to_flavour(int(flavour), row['time'])
        isodate = row['time'].date().isoformat()

        res['total'][isodate] += 1
        res['organisation'].setdefault(organisation, zeroed.copy())[isodate] += 1
        res['flavour'].setdefault(flavour, zeroed.copy())[isodate] += 1

    return make_response(req, res)

def slot_to_flavour(flavour, date=None):
    if date is None:
        date = datetime.datetime.now()

    # This is the config data for the slots. The first tuple member is the datetime from which the mapping (2nd element) is valid
    # IMPORTANT!!!! Dates have to be descending !!!!!
    conf = [
        # insert the new config HERE

        (datetime.datetime(2013, 9, 24), {1: 'Lungo Leggero', 2: 'Lungo Forte', 3: 'Lungo Forte', 4: 'Lungo Forte', 5: 'Espresso Forte', 6: 'Ristretto'}),
        (datetime.datetime(2012, 7, 13), {1: 'Lungo Leggero', 2: 'Lungo Forte', 3: 'Lungo Forte', 4: 'Espresso Leggero', 5: 'Espresso Forte', 6: 'Ristretto'}),
        (datetime.datetime(2011, 9, 2), {1: 'Lungo Leggero', 2: 'Lungo Forte', 3: 'Lungo Forte', 4: 'Espresso Leggero', 5: 'Espresso Forte', 6: 'Espresso Forte'}),
        (datetime.datetime(2000, 1, 1), {1: 'Ristretto', 2: 'Lungo Leggero', 3: 'Espresso Leggero', 4: 'Espresso Forte', 5: 'Espresso Decaffinato', 6: 'Espresso Decaffinato'}),
        # not here!!!
    ]

    for startdate, mapping in conf:
        if date > startdate:
            return mapping[flavour]
