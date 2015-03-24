
import sys, os, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'visapi')))

import logging
logging.basicConfig(level=logging.INFO)

import visapi.routing
application = visapi.routing.RpcDispatcher()

from visapi.apps import person, flags, beer, coffee
application.add_rpc("/person/lookup/<lookup>", person.get_person)
application.add_rpc("/person/search", person.search_by_name)
application.add_rpc("/flags/", flags.list_flags)
application.add_rpc("/flags/<flag>/", flags.search_flag)
application.add_rpc("/flags/<flag>/<uniqueid>", flags.get_flag_values)
application.add_rpc("/beer/status/<lookup>", beer.remaining)
application.add_rpc("/beer/status/<lookup>/dispensed", beer.dispensed)
application.add_rpc("/beer/stats/perday/monthly", beer.consumption_perday, days=30)
application.add_rpc("/beer/stats/histogram/monthly", beer.consumption_histogram, days=30)
application.add_rpc("/coffee/status/<lookup>", coffee.remaining)
application.add_rpc("/coffee/status/<lookup>/dispensed", coffee.dispensed)
application.add_rpc("/coffee/stats/detail/monthly", coffee.stats, days=30)
application.add_rpc("/coffee/stats/detail/<days>", coffee.stats) # new
application.add_rpc("/coffee/stats/perday/monthly", coffee.consumption_perday_detailed, days=30)
application.add_rpc("/coffee/stats/perday/yearly", coffee.consumption_perday, days=365)
application.add_rpc("/coffee/stats/perday_detailed/yearly", coffee.consumption_perday_detailed, days=365)
application.add_rpc("/coffee/stats/histogram/monthly", coffee.consumption_histogram, days=30)

from visapi.utils import get_config
config = get_config()

#
# authz
#

import visapps.authz
import visapps.authz.userrules
import visapps.authz.rulesdb
import visapps.authz.matching
import visapps.authz.combiners

import sesspy.sqlalchemy
import sesspy.config
visapi_rules_connector = sesspy.sqlalchemy.db_connection(
    db_uri=sesspy.config.ConfigOption(get_config, 'auth', 'db_uri'),
    engine_args=dict(pool_recycle=3600),
    name='visapi_rules_db',
)

rulesdb = visapps.authz.rulesdb.DbRules(rules_db=visapi_rules_connector)
userrules = visapps.authz.userrules.UserRules(rulesdb)

authzrule = visapps.authz.combiners.AnyNonDeny(
    userrules,
)

auth_realm = config.get('auth', 'realm')
def unauthorized(environ, start_response):
    body = 'Unauthorized.'
    headers= [
        ('WWW-Authenticate', 'Basic realm="%s"' % auth_realm),
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(body))),
    ]
    start_response('401 Unauthorized', headers)
    return [body]

application = authz_mw = visapps.authz.AuthorizationMiddleware(
    application, authzrule, unauthorized
)

#
# authn
#

import visapps.authn
import visapps.authn.basic
import visapps.authn.environ
import visapps.authn.krb

import vislib.lookup

class CustomLookup(object):
    def __init__(self, lookup_system=None):
        if lookup_system is None:
            lookup_system = vislib.lookup.system()
        self.lookup_system = lookup_system

    def get_role(self, identity):
        if '@' in identity:
            lookup, domain = identity.rsplit('@', 1)

            if domain == 'rfid.ethz.ch':
                return self.lookup_system.rfid.get_role(identity)

            elif domain == 'vis.ethz.ch' and not lookup.isdigit():
                return self.lookup_system.visldap.get_role(uid=lookup)

            elif domain == 'ethz.ch' and not lookup.isdigit():
                return self.lookup_system.nethz.get_role(uid=lookup)

            elif domain == 'forum.vis.ethz.ch':
                return self.lookup_system.inforum.get_role(identity)

            elif domain == 'inforum.ethz.ch':
                return self.lookup_system.inforum.get_role(identity)

            else:
                return self.lookup_system.uniqueid.get_role(identity)

        return self.lookup_system.visldap.get_role(uid=identity)

# password auth
application = authn_basic_mw = visapps.authn.basic.HttpBasicAuthn(
    CustomLookup(), "VIS Internal Area", application,
)

# ssl client certificate auth
application = authn_environ_mw = visapps.authn.environ.EnvironLookupAuthn(
    vislib.lookup.system().sslcn, application,
)

#application = authn_krb_mw = visapps.authn.krb.KerberosAuthn(
#    application, (lambda n: vislib.lookup.system().visldap.get_role(cn=n)),
#    principal='HTTP/www.vis.ethz.ch@VIS.ETHZ.CH'
#)

#
# misc
#

class SesspySessionCloser(object):
    def __init__(self, application):
        self.application = application
    def __call__(self, environ, start_response):
        import sesspy.session
        from werkzeug.wsgi import ClosingIterator
        sesspy.session.default_local_openers.close_remaining()
        res = self.application(environ, start_response)
        return ClosingIterator(res, [sesspy.session.default_local_openers.close_remaining])

application = SesspySessionCloser(application)

#
# debugging
#

class ExceptionLoggingMiddleware(object):
    def __init__(self, application):
        self.application = application
    def dispatch(self, environ, start_response):
        try:
            return self.application(environ, start_response)
        except Exception:
            logging.critical(
                'Uncaught exception while handling %s%s%s',
                environ.get('HTTP_HOST', ''),
                environ.get('SCRIPT_NAME', ''),
                environ.get('PATH_INFO', ''),
                exc_info=True
            )
            raise
    __call__ = dispatch
application = ExceptionLoggingMiddleware(application)

def setup_mailhandler(mailhost, to, subject):
    import pwd, socket
    import logging, logging.handlers
    user = pwd.getpwuid(os.getuid()).pw_name
    host = socket.getfqdn()
    mail_handler = logging.handlers.SMTPHandler(
        mailhost, user+'@'+host, to, subject
    )
    mail_handler.setLevel(logging.ERROR)
    logging.getLogger().addHandler(mail_handler)
setup_mailhandler('mail.vis.ethz.ch', 'webmaster@vis.ethz.ch', 'VISapi-Exception')

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 8081, application,
               use_reloader=True, use_debugger=True, use_evalex=True)

