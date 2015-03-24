
import vislib.flags
from visapi.rest.dec import restful
from visapi.rest import json, xml

list_xmlser_fmt = "<flags<flag*?&?>>"
@restful(accept=json.accept()+xml.accept_xmlser(list_xmlser_fmt),
         methods=["GET"])
def list_flags(req, args, make_response):
    all_flags = vislib.flags.list_flags()
    return make_response(req, all_flags)

search_xmlser_fmt = "<results<row*?<column*?<name&.0><value&.1>>>>"
@restful(accept=json.accept()+xml.accept_xmlser(search_xmlser_fmt),
         methods=["GET"])
def search_flag(req, args, make_response):
    flag = args['flag']
    search = dict(req.GET)
    search['flag'] = flag
    values = vislib.flags.search_flags(**search)
    return make_response(req, values)

values_xmlser_fmt = "<values<column*?<name&.0><value&.1>>>"
@restful(accept=json.accept()+xml.accept_xmlser(values_xmlser_fmt),
         methods=["GET"])
def get_flag_values(req, args, make_response):
    flag = args['flag']
    uniqueid = args['uniqueid']
    values = vislib.flags.get_flag_values(flag, uniqueid)
    return make_response(req, values)

