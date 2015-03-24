
from UserDict import DictMixin
import webob.exc

class ArgDict(DictMixin):

    def __init__(self, items=None):
        self._inner = dict(items or {})

    def __getitem__(self, name):
        try:
            return self._inner[name]
        except KeyError:
            raise webob.exc.HTTPBadRequest()

    def __contains__(self, name):
        return name in self._inner

    def __setitem__(self, name, value):
        self._inner[name] = value

    def __delitem__(self, name):
        del self._inner[name]

    def keys(self):
        return self._inner.keys()

    def iteritems(self):
        return self._inner.iteritems()
