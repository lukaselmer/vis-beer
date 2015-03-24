from visapi.utils import force_unicode
import webob
import webob.exc
import ordereddict

def pprint_response(req, obj):
    import pprint
    result = force_unicode(pprint.pformat(obj)).encode('utf-8')
    return webob.Response(body=result, status=200, content_type='text/plain', charset='utf-8')

def default_error_handler(req, e):
    import traceback
    error = force_unicode(traceback.format_exc()).encode('utf-8')
    return webob.Response(body=error, status=500, content_type='text/plain', charset='utf-8')

def get_accepted(req, accept):
    if accept is None:
        return ('text/plain', default_error_handler, pprint_response)
    accept = ordereddict.OrderedDict((a[0], a[1:]) for a in accept)
    mime_type = req.accept.best_match(accept.keys())
    if not mime_type:
        raise webob.exc.HTTPNotAcceptable()
    result = tuple([mime_type] + list(accept[mime_type]))
    return result

