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
    'single_instance':True,
    'webui':True,
    'api':True,
    'type':'downloader',
    'platform': ['Linux', 'Darwin', 'Windows']
}

CONFIG = ConfigList("sabnzbd", plugin=sys.modules[__name__], objects=[
    ConfigObject("enabled", "Enabled", "boolean", default=False, input_type="switch",
                 script=True),

    ConfigObject("downloadlocation", "Download Location", "string", default="downloads/",
                 help_text="Where is the completed download location?"),

    ConfigObject("host", "Host Location", "string", default="localhost",
                 help_text="Where is the sabnzbd website?"),

    ConfigObject("port", "Host Port", "integer", minimum=1001, maximum=65535, default=8080,
                 help_text="The Port where the host is located"),
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
