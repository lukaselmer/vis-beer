# -*- coding: utf-8 -*-
from __future__ import absolute_import
import webob

def make_response(req, xml, status=200):
    if isinstance(xml, unicode):
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml.encode('utf-8')
    res = webob.Response(body=xml, status=status, content_type=req.environ['visapi.accepted'])
    if res.content_type.startswith('text/'):
        res.charset = 'utf-8'
    return res

def get_xml_error(req, e):
    import traceback
    import sys
    from visapi.utils import force_unicode
    from xml.sax.saxutils import escape

    exc_type, exc_value, exc_tb = sys.exc_info()

    frames = ''.join(
        (u'\t\t<frame><file>%s</file><line>%s</line><function>%s</function><text>%s</text></frame>\n'
         % tuple([escape(force_unicode(o)) for o in frame]))
        for frame in traceback.extract_tb(exc_tb)
    )
    message = force_unicode(''.join(
        traceback.format_exception_only(exc_type, exc_value)
    )).rstrip()
    error = u'<error>\n' \
            u'\t<message>%s</message>\n' \
            u'\t<frames>\n' \
            u'%s' \
            u'\t</frames>\n' \
            u'</error>' % (escape(message), frames)
    return make_response(req, error, status=500)

def accept(response_builder):
    return [('application/xml', get_xml_error, response_builder),
            ('text/xml', get_xml_error, response_builder)]

def accept_serialized(serializer):
    def serialize_response(req, obj, status=200):
        return make_response(req, serializer(obj), status)
    return accept(serialize_response)

def accept_xmlser(xmlser_fmt):
    try:
        import xmlser
    except ImportError:
        from visapi import xmlser
    return accept_serialized(xmlser.make_serializer(xmlser_fmt))
