'''Movies controller init'''
from glob import glob
import sys
from configobj import ConfigObj
from validate import Validator
from libs.plugin_base import PluginBaseClass
from libs.config_list import ConfigList
from libs.config_object import ConfigObject
from .movies import MoviesLibrary
from . import www

SETTINGS = {
    'single_instance':False,
    'webui':True,
    'api':True,
    'type':'library',
    'platform': ['Linux', 'Darwin', 'Windows']
}

CONFIG = ConfigList("movies", plugin=sys.modules[__name__], objects=[
    ConfigObject("location", "Movies Location", "string", default="Library/Movies/",
                 help_text="Where is the library stored?")
])

class Plugin(PluginBaseClass):
    '''Main Class to create an instance of the plugin'''
    def startup(self):
        '''Startup Script'''
        self._system = MoviesLibrary(self._name, self._config, self._db)
        self._running = True
        return True, ""

    def shutdown(self):
        '''stop the plugin'''
        self._running = False
