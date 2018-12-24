'''Ripper Linux init'''
from glob import glob
import sys
import platform
import pathlib
from configobj import ConfigObj
from validate import Validator
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.plugin_base import PluginBaseClass
from libs.config_list import ConfigList
from libs.config_object import ConfigObject
from libs.config_rules import ConfigRules
from libs.sql.column import Column
from . import www
from .drive_linux import DriveLinux, get_hwinfo_linux
from .video import VIDEO_DB_INFO

#REQUIRED
# makemkv + java JRE + CCExtractor
# https://github.com/CCExtractor/ccextractor/blob/master/docs/COMPILATION.MD
#TODO MAKE SYSTEM OUTPUT A MESSAGE IF MISSING PROGRAMS FOR THIS SECTION TO RUN
#TODO add in options (for windows and mac for programs needed when they are worked on)
#TODO add in options for video ripping
#   audio languages/subtitles/closed-captions to keep
#   audio formats to keep
#   keep one audio/subtitle or multiple
#   keep extras
#   keep other videos
#TODO for the ripping/keep use bellow to show the videos so user can say what it is.
# <video controls width=800 autoplay>
#     <source src="file path here">
# </video>
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
    if platform.system() == 'Linux':
        pass
    return bool(DRIVES)

CONFIG = ConfigList("ripper", plugin=sys.modules[__name__], objects=[
    ConfigObject("enabled", "Enabled", "boolean", default=False, input_type="switch",
                 script=True),
    ConfigList("locations", "Folder Location", objects=[
        ConfigObject("videoripping", "Video Ripping Location", "string", default="videoripping/",
                     help_text="""
Where do you want to store video discs while ripping them?"""),
        ConfigObject("videoripped", "Video Ripped Location", "string", default="videoripped/",
                     help_text="""
Where do you want to move the video discs to when completed for librarys?"""),
        ConfigObject("audioripping", "Audio Ripping Location", "string", default="audioripping/",
                     help_text="""
Where do you want to store audio cds while ripping them?"""),
        ConfigObject("audioripped", "Audio Ripped Location", "string", default="audioripped/",
                     help_text="""
Where do you want to move the audio cds to when completed for librarys?""")
    ]),
    ConfigList("videoripping", "Video Ripping", objects=[
        ConfigObject("enabled", "Enabled", "boolean", default=True, input_type="switch",
                     script=True)
    ]),
    ConfigList("audioripping", "Audo CD Ripping", objects=[
        ConfigObject("enabled", "Enabled", "boolean", default=False, input_type="switch",
                     script=True)
    ]),
    ConfigList("drives", "Drives", objects=[
        ConfigObject("enabled", "Enabled", "boolean", default=False, input_type="switch",
                     script=True),
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
        self._db.table_check("Ripper",
                             VIDEO_DB_INFO["name"],
                             VIDEO_DB_INFO["data"],
                             VIDEO_DB_INFO["version"])

        for location in config['locations']:
            folder = config['locations'][location]
            if folder[0] != "/":
                folder = PROGRAMCONFIGLOCATION + config['locations'][location]
            pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

    def startup(self):
        '''Ripper Startup Script'''
        if platform.system() == 'Linux':
            for drive in DRIVES:
                if drive in self._config['drives']:
                    if self._config['drives'][drive]["enabled"]:
                        self._drives.append(DriveLinux(DRIVES[drive], self._config, self._db))

        #Check if Devices Exist and if not it will stop the plugin from loading
        if not self._drives:
            return False, "No Optical Devices Found or enabled"

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
