'''Ripper Linux init'''
from glob import glob
import sys
from configobj import ConfigObj
from validate import Validator
from libs.plugin_base import PluginBaseClass
from libs.config_list import ConfigList
from libs.config_object import ConfigObject
from .drive_control import Drive
from . import www

#TODO SPLIT THIS UP INTO PARTS OF THE SYSTEM FOR MORE CUSTOMIZABILITY
#TODO MAKE SYSTEM OUTPUT A MESSAGE IF MISSING PROGRAMS FOR THIS SECTION TO RUN

SETTINGS = {
    'single_instance':True,
    'webui':True,
    'api':True,
    'type':'ripping',
    'platform': ['Linux']#, 'Darwin', 'Windows']
}

def check_enabled():
    '''plugin check for if plugin should be enabled'''
    return bool(glob('/dev/sr*'))

CONFIG = ConfigList("ripper", sys.modules[__name__])
CONFIG.append(
    ConfigObject("enabled", "Enabled", "boolean", default=False, input_type="switch",
                 help_text="Is the System Enabled", script=True)
)
CONFIG.append(
    ConfigObject("convert", "Convert", "boolean", default=True, input_type="switch",
                 help_text="Do you want the Video Converted after ripping?", priority=1)
)
CONFIG.append(
    ConfigObject("ripping", "Ripping Location", "string", config_group="locations",
                 default="ripping/",
                 help_text="Where do you want to store discs while ripping them?")
)
CONFIG.append(
    ConfigObject("ripped", "Ripped Location", "string", config_group="locations",
                 default="ripped/",
                 help_text="""
Where do you want to move the discs to when completed for librarys?""")
)

class Plugin(PluginBaseClass):
    '''Main Class to create an instance of the plugin'''

    def __init__(self, plugin_link, name, config, db):
        super().__init__(plugin_link, name, config, db)
        self._drives = []

    ##need to sort out the ripper print function use a log system with thread safe usage.
    ##need to fix ripper.run function so it works better
    ## and will not get stuck within a wait function.
    def startup(self):
        '''Ripper Startup Script'''
        #Check if Devices Exist and if not it will stop the plugin from loading
        self._drives = [Drive(d, self._db) for d in glob('/dev/sr*')]
        if not self._drives:
            return False, "No Optical Devices Found"

        #Start the threads
        for drive in self._drives:
            drive.start_thread()

        self._running = True
        return True, ""

    def shutdown(self):
        '''stop the plugin'''
        for drive in self._drives:
            drive.stop_thread()
        self._running = False
