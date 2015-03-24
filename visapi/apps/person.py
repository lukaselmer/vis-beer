
import vislib.person
import webob.exc
import sesspy.ref
from visapi.rest.dec import restful
from visapi.rest import json, xml

person_data_xmlser_fragment_fmt = "<.0*?~.0=phonenumbers{.1<phone*?&?>}~~.0=groups{.1<group*?&?>}~~.1?&.1>"

person_xmlser_fmt = "<person%s>" % person_data_xmlser_fragment_fmt
@restful(accept=json.accept()+xml.accept_xmlser(person_xmlser_fmt),
         methods=["GET"])
def get_person(req, args, make_response):
    lookup = args['lookup']
    try:
        person = vislib.person.get_person(lookup)
    except vislib.person.InvalidPerson:
        raise webob.exc.HTTPNotFound()
    person_data = person.__getstate__()
    return make_response(req, person_data)

search_by_name_xmlser_fmt = "<results<person*?%s>>" % person_data_xmlser_fragment_fmt
@restful(accept=json.accept()+xml.accept_xmlser(search_by_name_xmlser_fmt),
         methods=["GET"])
def search_by_name(req, args, make_response):
    gnset = 'givenname' in req.GET
    snset = 'surname' in req.GET

    if gnset and not snset:
        search = {'givenName': req.GET['givenname'].encode('utf-8')}
    elif snset and not gnset:
        search = {'surname': req.GET['surname'].encode('utf-8')}
    elif gnset and snset:
        search = {
            'givenName': req.GET['givenname'].encode('utf-8'),
            'surname': req.GET['surname'].encode('utf-8'),
        }
    else:
        raise webob.exc.HTTPBadRequest("Must supply givenname or surname query arguments")

    nethzldap_ref = sesspy.ref.ComponentRef('nethzldap')
    with nethzldap_ref() as nethzldap:
        result = nethzldap.get(**search)
    persons = []
    for entry in result:
        try:
            persons.append(vislib.person.get_person(entry[1]).__getstate__())
        except Exception:
            pass

    return make_response(req, persons)
