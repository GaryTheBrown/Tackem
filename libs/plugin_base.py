'''MySQL Abstract Class System'''
from abc import ABCMeta, abstractmethod

class PluginBaseClass(metaclass=ABCMeta):
    '''base class of the plugins'''

    def __init__(self, plugin_link, name, config, root_config, db, musicbrainz):
        self._running = False
        self._system = None
        self._plugin_link = plugin_link
        self._name = name
        self._config = config
        self._root_config = root_config
        self._db = db
        self._musicbrainz = musicbrainz

    @abstractmethod
    def startup(self):
        '''Startup Script'''

    @abstractmethod
    def shutdown(self):
        '''stop the plugin'''

    def running(self):
        '''is it running?'''
        return self._running

    def name(self):
        '''Returns the Plugin Name'''
        return self._name

    def plugin_link(self):
        '''Returns the plugin Link'''
        return self._plugin_link
