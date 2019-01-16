'''Ripper Linux init'''
import sys
import platform
import pathlib
import threading
from configobj import ConfigObj
from validate import Validator
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.plugin_base import PluginBaseClass
from libs.config_list import ConfigList
from libs.config_object import ConfigObject
from libs.config_option import ConfigOption
from libs.config_rules import ConfigRules
from libs.data.language_options import OPTIONS as language_options
from libs.data.audio_format_options import OPTIONS as audio_format_options
from . import www
from .data import db_tables
from .data.events import RipperEvents
from .drive_linux import DriveLinux, get_hwinfo_linux
from .converter import Converter
from .renamer import Renamer

#REQUIRED
# makemkv + java JRE + CCExtractor libcss2
# sudo apt install libdvd-pkg && sudo dpkg-reconfigure libdvd-pkg
# https://github.com/CCExtractor/ccextractor/blob/master/docs/COMPILATION.MD
# TODO MAKE SYSTEM OUTPUT A MESSAGE IF MISSING PROGRAMS FOR THIS SECTION TO RUN
# for the ripping/keep use bellow to show the videos so user can say what it is.

# makemkv settings.conf
# app_DefaultOutputFileName = "{t:N2}"
# app_ExpertMode = "1"
# app_Java = ""
# app_ccextractor = "/usr/local/bin/ccextractor"

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
Where do you want to move the video discs to when completed"""),
        ConfigObject("audioripping", "Audio Ripping Location", "string", default="audioripping/",
                     help_text="""
Where do you want to store audio cds while ripping them?"""),
        ConfigObject("audioripped", "Audio Ripped Location", "string", default="audioripped/",
                     help_text="""
Where do you want to move the audio cds to when completed""")
    ]),
    ConfigList("videoripping", "Video Ripping", objects=[
        ConfigObject("enabled", "Enabled", "boolean", default=True, input_type="switch",
                     script=True),
        ConfigObject("torip", "What to Rip", "string_list", default=["movie", "tvshow"],
                     input_type="checkbox", options=[
                         ConfigOption("movie", "Movie"),
                         ConfigOption("tvshow", "TV Show Episode"),
                         ConfigOption("trailer", "Trailer"),
                         ConfigOption("extra", "Extra"),
                         ConfigOption("other", "Other")
                     ],
                     help_text="What File Types do you want to rip and include"),
    ]),
    ConfigList("audioripping", "Audo CD Ripping", objects=[
        ConfigObject("enabled", "Enabled", "boolean", default=False, input_type="switch",
                     script=True)
    ]),
    ConfigList("converter", "Converter", objects=[
        ConfigObject("enabled", "Enabled", "boolean", default=True, input_type="switch",
                     script=True),
        ConfigObject("ffmpeglocation", "FFmpeg Location", "string", default="ffmpeg",
                     help_text="Where is FFmpeg located?"),
        ConfigObject("ffprobelocation", "FFprobe Location", "string", default="ffprobe",
                     help_text="Where is FFprobe located?"),
        ConfigObject("threadcount", "How Many Instances?", "integer", minimum=1, maximum=5,
                     default=1, help_text="How Many Threads (Max of 5)"),
        ConfigObject("videoresolution", "Max Video Resolution", "option", default='keep',
                     input_type='radio',
                     options=[
                         ConfigOption("keep", "Keep Original"),
                         ConfigOption("2160", "4K"),
                         ConfigOption("1080", "1080"),
                         ConfigOption("720", "720"),
                         ConfigOption("sd", "SD")],
                     help_text="What is the maximum resolution you want to keep or downscale to?"),
        ConfigObject("videocodec", "Video Codec", "option", default='keep',
                     input_type='radio',
                     options=[
                         ConfigOption("keep", "Keep Original"),
                         ConfigOption("x264default", "X264 Default"),
                         ConfigOption("x265default", "X265 Default"),
                         ConfigOption("x264custom", "X264 Custom"),
                         ConfigOption("x265custom", "X265 Custom")],
                     help_text="What video codec do you wish to convert to?"),
        # video codec
        # https://matroska.org/technical/specs/codecid/index.html
        # think about being able to combine videos into 1 file
        # think about HDR -> https://forum.doom9.org/showthread.php?t=175227
        ConfigObject("defaultlanguage", "Default Language", "string",
                     input_type="dropdown", options=language_options,
                     help_text="What is your main language?"),
        ConfigObject("originalordub", "Original or Dubbed Language", "option", default='all',
                     input_type='radio', options=[ConfigOption("original", "Original"),
                                                  ConfigOption("dub", "Dubbed")],
                     help_text="""
Do you want the default stream to be the Original language or dubbed in your language if available?
"""),
        ConfigObject("audiolanguage", "Audio Languages", "option", default='all',
                     input_type='radio',
                     options=[ConfigOption("all", "All",
                                           hide="plugins_ripping_ripper_converter_audiolanglist"),
                              ConfigOption("original", "Original Language Only",
                                           hide="plugins_ripping_ripper_converter_audiolanglist"),
                              ConfigOption("selectedandoriginal",
                                           "Original Language + Selected Languages",
                                           show="plugins_ripping_ripper_converter_audiolanglist"),
                              ConfigOption("selected", "Selected Languages",
                                           show="plugins_ripping_ripper_converter_audiolanglist")],
                     help_text="What Audio Languages do you want to keep?"),
        ConfigList("audiolanglist", "Audio Language List", objects=[
            ConfigObject("audiolanguages", "Audio Languages", "string_list",
                         input_type="checkbox", options=language_options)],
                   is_section=True, section_link=["plugins", "ripping", "ripper",
                                                  "converter", "audiolanguage"]),
        ConfigObject("audioformat", "Audio Format", "option", default='all',
                     input_type='radio',
                     options=[
                         ConfigOption("all", "All",
                                      hide="plugins_ripping_ripper_converter_audioformatlist"),
                         ConfigOption("highest", "Highest Quality",
                                      hide="plugins_ripping_ripper_converter_audioformatlist"),
                         ConfigOption("selected", "Selected Formats",
                                      show="plugins_ripping_ripper_converter_audioformatlist")],
                     help_text="What Audio Formats do you want to keep?"),
        ConfigList("audioformatlist", "Audio Format List", objects=[
            ConfigObject("audioformats", "Audio Formats", "string_list",
                         input_type="checkbox", options=audio_format_options)],
                   is_section=True, section_link=["plugins", "ripping", "ripper",
                                                  "converter", "audioformat"]),
        ConfigObject("keepcommentary", "Keep Commentary", "boolean", default=True,
                     input_type="checkbox", help_text="""
Do you want to keep the commentary track(s)?"""),
        #Audio conversion section here (defaulted to off) if user wants to add audio formats
        #   ConfigOption("convert", "Convert to Selected Formats",
        #                show="plugins_ripping_ripper_converter_audioformatlist"),
        ConfigObject("keepchapters", "Keep Chapters", "boolean", default=True,
                     input_type="checkbox", help_text="""
Do you want to keep the chapter points?"""),
        ConfigObject("subtitle", "Subtitles", "option", default='all', input_type='radio',
                     options=[ConfigOption("all", "All",
                                           hide="plugins_ripping_ripper_converter_subtitleslist"),
                              ConfigOption("none", "None",
                                           hide="plugins_ripping_ripper_converter_subtitleslist"),
                              ConfigOption("selected", "Selected Subtitles",
                                           show="plugins_ripping_ripper_converter_subtitleslist")],
                     help_text="What subtitles do you want to keep?"),
        ConfigList("subtitleslist", "Subtitle List", objects=[
            ConfigObject("subtitlelanguages", "Subtitle Languages", "string_list",
                         input_type="checkbox", options=language_options)],
                   is_section=True, section_link=["plugins", "ripping", "ripper",
                                                  "converter", "subtitle"]),
        ConfigObject("keepclosedcaptions", "Keep Closed Captions", "boolean", default=True,
                     input_type="checkbox", help_text="Do you want to keep the closed captions?"),
    ]),
    ConfigList("drives", "Drives", objects=[
        ConfigObject("enabled", "Enabled", "boolean", default=False, input_type="switch",
                     script=True),
        ConfigObject("name", "Name", "string", default="",
                     help_text="What do you want to call this drive?"),
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
        self._events = RipperEvents()
        self._converter = None
        self._renamer = None

        self._db.table_check("Ripper",
                             db_tables.VIDEO_INFO_DB_INFO["name"],
                             db_tables.VIDEO_INFO_DB_INFO["data"],
                             db_tables.VIDEO_INFO_DB_INFO["version"])
        self._db.table_check("Ripper",
                             db_tables.VIDEO_CONVERT_DB_INFO["name"],
                             db_tables.VIDEO_CONVERT_DB_INFO["data"],
                             db_tables.VIDEO_CONVERT_DB_INFO["version"])

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
                        self._drives.append(DriveLinux(drive, DRIVES[drive],
                                                       self._config, self._db))

        #Check if Devices Exist and if not it will stop the plugin from loading
        if not self._drives:
            return False, "No Optical Devices Found or enabled"

        #Start the threads
        for drive in self._drives:
            drive.start_thread()

        if self._config['converter']['enabled']:
            self._converter = Converter(self._config, self._db)
            self._converter.start_thread()

        print("START RENAMER THREAD")
        self._renamer = Renamer(self._config, self._db)
        self._renamer.start_thread()

        self._running = True
        return True, ""

    def shutdown(self):
        '''stop the plugin'''
        for drive in self._drives:
            drive.unlock_tray()
            drive.stop_thread()
        if self._converter is not None:
            self._events.converter.set()
            self._converter.stop_thread()
        if self._renamer is not None:
            self._events.renamer.set()
            self._renamer.stop_thread()
        self._running = False

    def get_drives(self):
        '''gets the drives'''
        return self._drives
