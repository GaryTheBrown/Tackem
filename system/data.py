'''System Data'''
import threading

class SystemData():
    '''System Data'''
    plugins = {} # [type][ name]
    plugins_lock = threading.Lock()
    systems = {} # [type name]
    systems_lock = threading.Lock()
    plugin_cfg = {} # [type name]
    plugin_cfg_lock = threading.Lock()
    config = None
    config_lock = threading.Lock()
    sql = None
    webserver = None
    auth = None
    musicbrainz = None
