
def force_unicode(txt):
    try:
        return unicode(txt)
    except UnicodeDecodeError:
        pass
    orig = txt
    if type(txt) != str:
        txt = str(txt)
    for args in [('utf-8',), ('latin1',), ('ascii', 'replace')]:
        try:
            return txt.decode(*args)
        except UnicodeDecodeError:
            pass
    raise ValueError("Unable to force %s object %r to unicode" % (type(orig).__name__, orig))

config = None
config_paths = ['/etc/visapi', '/etc/vis/visapi', '~/.config/visapi', '~/.config/vis/visapi']
def get_config():
    global config
    import os.path
    if not config:
        import ConfigParser
        config_ = ConfigParser.RawConfigParser()
        config_.read(os.path.expanduser(p) for p in config_paths)
        config = config_
    return config
