'''Movies controller init'''
from glob import glob
import sys
from configobj import ConfigObj
from validate import Validator
from libs.plugin_base import PluginBaseClass
from libs.config_list import ConfigList
from libs.config_object import ConfigObject
from . import www

# HOW to change modal input to a select box
#
SETTINGS = {
    'single_instance':False,
    'webui':True,
    'api':True,
    'type':'library',
    'platform': ['Linux', 'Darwin', 'Windows'],
    'list_of_options':[
        'SNES', 'NES'
    ]
}

CONFIG = ConfigList("games", plugin=sys.modules[__name__], objects=[
    ConfigObject("location", "Game Location", "string", default="Library/Games/",
                 help_text="Where is the library stored?")
])

class Plugin(PluginBaseClass):
    '''Main Class to create an instance of the plugin'''
    def startup(self):
        '''Startup Script'''
        self._running = True
        return True, ""

    def shutdown(self):
        '''stop the plugin'''
        self._running = False
