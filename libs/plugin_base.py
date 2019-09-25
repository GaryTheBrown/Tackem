'''MySQL Abstract Class System'''
import json
from abc import ABCMeta, abstractmethod
from system.plugin import TackemSystemPlugin

class PluginBaseClass(metaclass=ABCMeta):
    '''base class of the plugins'''

    def __init__(self, system_name, single_instance=False):
        self._running = False
        self._system = None
        self._name = system_name
        instance = None
        name_split = system_name.split(" ")
        if single_instance:
            plugin_type = name_split[-2]
            plugin_name = name_split[-1]
        else:
            plugin_type = name_split[-3]
            plugin_name = name_split[-2]
            instance = name_split[-1]

        self._tackem_system = TackemSystemPlugin(plugin_type, plugin_name, instance)

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
        return self._tackem_system.plugin()

def load_plugin_settings(settings_json_file):
    '''function to load the plugin settings.json'''
    with open(settings_json_file, 'r') as json_file:
        settings = json.load(json_file)
    return settings
