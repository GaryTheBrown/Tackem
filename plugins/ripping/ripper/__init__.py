'''Ripper Linux init'''
from glob import glob
import sys
import platform
from configobj import ConfigObj
from validate import Validator
from libs.plugin_base import PluginBaseClass
from libs.config_list import ConfigList
from libs.config_object import ConfigObject
from libs.config_rules import ConfigRules
from libs.sql.column import Column
from . import www
from .drive_linux import DriveLinux, get_hwinfo_linux

#TO DO SPLIT THIS UP INTO PARTS OF THE SYSTEM FOR MORE CUSTOMIZABILITY
#TO DO MAKE SYSTEM OUTPUT A MESSAGE IF MISSING PROGRAMS FOR THIS SECTION TO RUN
#TO DO add in other options for individual drives including what it can read.
# maybe have the what it can read auto fill if possible.
# need to sort out the ripper print function use a log system with thread safe usage.
# need to fix ripper.run function so it works better
# and will not get stuck within a wait function.

SETTINGS = {
    'single_instance':True,
    'webui':True,
    'api':True,
    'type':'ripping',
    'platform': ['Linux']#, 'Darwin', 'Windows']
}
DRIVES = {}
if platform.system() == 'Linux':
    DRIVES = get_hwinfo_linux()

def check_enabled():
    '''plugin check for if plugin should be enabled'''
    return bool(DRIVES)

CONFIG = ConfigList("ripper", sys.modules[__name__], objects=[
    ConfigObject("enabled", "Enabled", "boolean", default=False, input_type="switch",
                 help_text="Is the System Enabled", script=True),
    ConfigObject("ripfromdisc", "Rip From Disc", "boolean", default=True, input_type="switch",
                 help_text="""Do you want the ripper to rip straight from the disc.
Turn this off if you want it to rip the disc to an ISO on the drive before ripping the files"""),
    ConfigList("locations", objects=[
        ConfigObject("ripping", "Ripping Location", "string", default="ripping/", help_text="""
Where do you want to store discs while ripping them?"""),
        ConfigObject("ripped", "Ripped Location", "string", default="ripped/", help_text="""
Where do you want to move the discs to when completed for librarys?""")
    ]),
    ConfigList("drives", objects=[
        ConfigObject("enabled", "Enabled", "boolean", default=False, input_type="switch",
                     help_text="Is the System Enabled", script=True),
        ConfigObject("link", "Drive Link", "string", read_only=True, disabled=True,
                     not_in_config=True, value_link=DRIVES,
                     help_text="Adderss of the drive"),
        ConfigObject("model", "Drive Model", "string", read_only=True, disabled=True,
                     not_in_config=True, value_link=DRIVES,
                     help_text="Adderss of the drive")
    ], rules=ConfigRules(for_each=DRIVES))
])

class Plugin(PluginBaseClass):
    '''Main Class to create an instance of the plugin'''

    def __init__(self, plugin_link, name, config, root_config, db):
        super().__init__(plugin_link, name, config, root_config, db)
        self._drives = []

    def startup(self):
        '''Ripper Startup Script'''
        # if platform.system() == 'Linux':
        #     self._drives = [DriveLinux(d, self._config, self._db) for d in DRIVES]

        # #Check if Devices Exist and if not it will stop the plugin from loading
        # if not self._drives:
        #     return False, "No Optical Devices Found"

        # #Start the threads
        # for drive in self._drives:
        #     drive.start_thread()

        self._running = True
        return True, ""

    def shutdown(self):
        '''stop the plugin'''
        # for drive in self._drives:
        #     drive.stop_thread()
        self._running = False
