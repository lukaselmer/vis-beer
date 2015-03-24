# -*- coding: utf-8 -*-
from __future__ import absolute_import

import visapi.argdict
from visapi.rest.accept import get_accepted
from functools import wraps
from webob.dec import wsgify
import webob.exc
from werkzeug.wsgi import ClosingIterator

def restful(accept=None, methods=None):
    def restful_dec(f):
        @wraps(f)
        @wsgify
        def do_restful(req):
            if methods and req.method not in methods:
                raise webob.exc.HTTPMethodNotAllowed()
            if 'visapi.args' not in req.environ:
                req.environ['visapi.args'] = visapi.argdict.ArgDict()
            accepted, error_handler, response_builder = get_accepted(req, accept)
            req.environ['visapi.accepted'] = accepted
            try:
                return f(req, req.environ['visapi.args'], response_builder)
            except webob.exc.HTTPException:
                raise
            except Exception as e:
                return error_handler(req, e)
        # automatically handle HEAD if necessary
        if methods and "GET" in methods and "HEAD" not in methods:
            return handle_head(do_restful)
        else:
            return do_restful
    return restful_dec

def handle_head(f):
    @wraps(f)
    def do_handling_head(environ, start_response):
        if environ['REQUEST_METHOD'] != "HEAD":
            return f(environ, start_response)
        else:
            # create new environment with GET request method
            get_request_environ = dict(environ)
            get_request_environ['REQUEST_METHOD'] = "GET"
            # create start_response that sets Content-Length to 0
            def start_head_response(status, headers):
                new_headers = []
                for name, value in headers:
                    if name.lower() == 'content-length':
                        new_headers.append(('Content-Length', '0'))
                    else:
                        new_headers.append((name, value))
                start_response(status, new_headers)
            # get response data and discard, but make sure to close the iterator
            body_iter = f(get_request_environ, start_head_response)
            if hasattr(body_iter, 'close'):
                return ClosingIterator([], body_iter.close)
            else:
                return []
    return do_handling_head
