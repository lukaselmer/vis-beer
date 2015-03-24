import werkzeug.routing
import werkzeug.exceptions
import webob.exc
import argdict

class RpcDispatcher(object):

    def __init__(self):
        self.url_map = werkzeug.routing.Map()
        self.handlers = {}

    def add_rpc(self, rule, rpc, **default_args):
        self.url_map.add(werkzeug.routing.Rule(rule, endpoint=rule))
        self.handlers[rule] = (rpc, default_args)

    def dispatch(self, environ, start_response):
        url_adapter = self.url_map.bind_to_environ(environ)

        try:
            rule, args = url_adapter.match()
        except werkzeug.exceptions.HTTPException as e:
            response = e
        except webob.exc.HTTPException as e:
            response = e
        else:
            response, default_args = self.handlers[rule]
            args = dict(default_args, **args)
            environ['visapi.args'] = argdict.ArgDict(args)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.dispatch(environ, start_response)

