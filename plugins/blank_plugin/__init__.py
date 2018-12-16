'''sabnzbd controller init'''
from glob import glob
import sys
from configobj import ConfigObj
from validate import Validator
from libs.plugin_base import PluginBaseClass
from libs.config_list import ConfigList
from libs.config_object import ConfigObject
from . import www

SETTINGS = {
    'single_instance':True, # INSTANCE TYPE 'single', 'multi', 'multi_list'
    'webui':False, # IF THE SYSTEM HAS A WEBUI (CONFIG IS SEPERATE AS PULLED FOR THE ROOT SYSTEM)
    'api':False, # IF THIS SYSTEM WORKS WITH API CONTROLS
    'type':'library', # library, downloader, searcher
}
CONFIG = ConfigList("", sys.modules[__name__])

class Plugin(PluginBaseClass):
    '''Main Class to create an instance of the plugin'''
    def startup(self):
        '''Startup Script'''
        self._running = True
        return True, ""

    def shutdown(self):
        '''stop the plugin'''
        self._running = False
        return True
