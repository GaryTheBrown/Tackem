'''Ripper Linux init'''
from glob import glob
import sys
from configobj import ConfigObj
from validate import Validator
from libs.plugin_base import PluginBaseClass
from libs.config_list import ConfigList
from libs.config_object import ConfigObject
from libs.config_rules import ConfigRules
from .drive_control import Drive
from . import www

#TO DO SPLIT THIS UP INTO PARTS OF THE SYSTEM FOR MORE CUSTOMIZABILITY
#TO DO MAKE SYSTEM OUTPUT A MESSAGE IF MISSING PROGRAMS FOR THIS SECTION TO RUN

SETTINGS = {
    'single_instance':True,
    'webui':True,
    'api':True,
    'type':'ripping',
    'platform': ['Linux']#, 'Darwin', 'Windows']
}
#TODO MAKE A LIST FOR THE CONFIG SO EACH DRIVE HAS MORE INFO TO USE TO STORE IT IN THE CONFIG INCASE
# OF DRIVES BEING MOVED IN THE SYSTEM CHANGING THERE NUMBERS
DRIVES = glob('/dev/sr*')

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
    # ConfigList("drives", objects=[
    #     ConfigObject("enabled", "Enabled", "boolean", default=False, input_type="switch",
    #                  help_text="Is the System Enabled", script=True),
    #     ConfigObject("label", "Drive Label", "string", default="",
    #                  help_text="Label for easy recognition of drive in program")
    # ], rules=ConfigRules(for_each=DRIVES))
])
# TO DO add in other options for individual drives including what it can read.
# maybe have the what it can read auto fill if possible.

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
        self._drives = [Drive(d, self._db) for d in DRIVES]
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
