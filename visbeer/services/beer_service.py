import re
import datetime
import math
from visbeer.services.data_service import DataService

ENABLE_BEER_CONSUMPTION = True
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_BEERS_PER_DAY = 1
RFID_REGEX = re.compile(r"[0-9]{6}@rfid\.ethz\.ch")


def beginning_of_current_day():
    cutoff = datetime.time(3, 0)
    if datetime.datetime.now().time() < cutoff:
        day = datetime.date.today() - datetime.timedelta(days=1)
    else:
        day = datetime.date.today()
    return datetime.datetime.combine(day, cutoff)


def validate_rfid(rfid):
    if not RFID_REGEX.match(rfid):
        raise Exception('Invalid rfid')


class BeerService:
    def __init__(self, rfid, data_service=DataService()):
        validate_rfid(rfid)

        self.rfid = rfid
        self.data_service = data_service
        self.person = data_service.find_person(rfid)

    def status(self):
        if not ENABLE_BEER_CONSUMPTION and not self.no_limit():
            # enable API testing even if the beer consumption is disabled
            return 0

        if not self.person.vismember:
            # allow only vis members to drink beer
            return 0

        if not self.has_consumed_today():
            # no consumption today -> reset the remaining value
            self.data_service.set_flag_value(self.person, 'remaining', self.beers_per_day())

        return self.get_remaining()

    def dispensed(self):
        return self.status()

    def no_limit(self):
        return self.data_service.get_flag_value(self.person, 'nolimit')

    def beers_per_day(self):
        self.data_service.set_default_flag_value(self.person, 'perday', DEFAULT_BEERS_PER_DAY)
        return self.data_service.get_flag_value(self.person, 'perday')

    def get_remaining(self):
        remaining_beers = int(self.data_service.get_flag_value(self.person, 'remaining') or self.beers_per_day())
        # for every 2 coffees, subtract on beer (at least)
        beers_exchanged_for_coffee = int(math.ceil(self.dispensed_coffees_today() / 2.0))
        return max(0, remaining_beers - beers_exchanged_for_coffee)

    def dispensed_coffees_today(self):
        # TODO: make data service coffee or beer specific
        if self.has_consumed_today():
            return int(self.data_service.get_flag_value(self.person, 'dispensed_today') or 0)
        return 0

    def has_consumed_today(self):
        last_consumption_str = self.data_service.get_flag_value(self.person, 'last')

        if not last_consumption_str:
            # this is the case if someone never consumed a beverage until now
            return False

        last_consumption = datetime.datetime.strptime(last_consumption_str, DATETIME_FORMAT)
        if not last_consumption:
            # format error -> assume there was no consumption today
            return False

        return last_consumption >= beginning_of_current_day()
