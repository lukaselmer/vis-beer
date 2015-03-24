# -*- coding: utf-8 -*-
from __future__ import absolute_import
import webob
from visapi.utils import force_unicode
try:
    import json as json_
except ImportError:
    import simplejson as json_

def _default_handler(o):
    if hasattr(o, 'iteritems'):
        return dict(o.iteritems())
    elif hasattr(o, '__iter__'):
        return list(o)
    else:
        return force_unicode(o)

def make_response(req, obj, status=200):
    s = json_.dumps(obj, default=_default_handler)

    if 'jsonp_callback' in req.GET:
        s = req.GET['jsonp_callback'].encode('ascii') + '(' + s + ');'

    res = webob.Response(body=s, status=status, content_type=req.environ['visapi.accepted'])
    if res.content_type.startswith('text/'):
        res.charset = 'utf-8'
    return res

def get_json_error(req, e):
    import traceback
    import sys

    exc_type, exc_value, exc_tb = sys.exc_info()

    frames = [dict(file=f[0], line=f[1], function=f[2], text=f[3])
              for f in [
                  [force_unicode(o) for o in frame]
                  for frame in traceback.extract_tb(exc_tb)
              ]]
    trace = force_unicode(traceback.format_tb(exc_tb))
    message = force_unicode(''.join(
        traceback.format_exception_only(exc_type, exc_value)
    )).rstrip()
    error = dict(message=message, trace=trace, frames=frames)
    return make_response(req, error, status=500)

def accept(response_builder=make_response):
    return [('application/json', get_json_error, response_builder),
            ('text/json', get_json_error, response_builder)]

