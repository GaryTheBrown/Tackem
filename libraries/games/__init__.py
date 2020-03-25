'''Movies controller init'''
from libs.plugin_base import PluginBaseClass, load_plugin_settings
from . import www

class Plugin(PluginBaseClass):
    '''Main Class to create an instance of the plugin'''

    def startup(self):
        '''Startup Script'''
        self._running = True
        return True, ""

    def shutdown(self):
        '''stop the plugin'''
        self._running = False
