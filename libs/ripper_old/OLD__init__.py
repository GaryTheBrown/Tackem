'''Ripper Linux init'''
import platform

from data import PROGRAMCONFIGLOCATION, PLUGINFOLDERLOCATION
from libs.plugin_base import PluginBaseClass, load_plugin_settings

from libs.database import Database
from libs.database.messages import SQLTable
from libs.hardware import Hardware
from data.config import CONFIG as ROOT_Config
from . import www
from .data import db_tables
from .data.events import RipperEvents
from .drive_linux import DriveLinux
from .video_labeler import VideoLabeler
from .converter import Converter
from .renamer import Renamer

# SETTINGS = load_plugin_settings(
#     PLUGINFOLDERLOCATION + "ripping/ripper/settings.json")
# DRIVES = {}

# if platform.system() == 'Linux':
    # if check_for_required_programs(SETTINGS['linux_programs'], output=False):
        # DRIVES = get_hwinfo_linux()


# def check_enabled():
#     '''plugin check for if plugin should be enabled'''
#     if platform.system() == 'Linux':
#         if not check_for_required_programs(SETTINGS['linux_programs'], "Ripper"):
#             return False
#     return bool(DRIVES)


class Ripper:
    '''Main Class to create an instance of the plugin'''

    def __init__(self):
        pass


    def startup(self):
        '''Ripper Startup Script'''
        if platform.system() == 'Linux':
            for dri in Hardware.disc_drives():
                if dri in ROOT_Config['ripper']['drives']:
                    if ROOT_Config['ripper']['drives'][dri]["enabled"].value:
                        self._drives.append(DriveLinux(dri, Hardware.disc_drives()[dri]))

        # Check if Devices Exist and if not it will stop the plugin from loading
        if not self._drives:
            return False, "No Optical Devices Found or enabled"

        # Start the threads
        for drive in self._drives:
            drive.start_thread()

        if ROOT_Config['ripper']['converter']['enabled'].value:
            self._converter.start_thread()

        print("START RENAMER THREAD")
        self._renamer.start_thread()

        self._running = True
        return True, ""

    def shutdown(self):
        '''stop the plugin'''
        for drive in self._drives:
            drive.unlock_tray()
            drive.stop_thread()
        if self._converter is not None:
            RipperEvents().converter.set()
            self._converter.stop_thread()
        if self._renamer is not None:
            RipperEvents().renamer.set()
            self._renamer.stop_thread()
        self._running = False

    def get_drives(self):
        '''gets the drives'''
        return self._drives

    def get_video_labeler(self):
        '''returns the video_labeler system'''
        return self._video_labeler

    def get_converter(self):
        '''returns the converter system'''
        return self._converter
