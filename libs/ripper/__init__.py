'''Ripper init'''
from data.database.ripper import AUDIO_CONVERT_DB_INFO, AUDIO_INFO_DB_INFO
from data.database.ripper import VIDEO_CONVERT_DB_INFO, VIDEO_INFO_DB_INFO
import platform
from data.config import CONFIG
from libs.classproperty import classproperty
from libs.database import Database
from libs.database.messages.table import SQLTable
from libs.file import File
from libs.hardware import Hardware
from libs.ripper.drive_linux import DriveLinux

# TODO Pull Ripper plugin back into the System with checks for programs to load system then checks
# on if drives exist and give the option of ripping locally or just giving ISO
# TODO Allow ripper to just accept ISOs instead if no drives in the machine.
# then we can create some api call to say there is a new ISO to work with,
# would need to check the process of getting info from the bluray for it's codes we are using.
# a seperate system for ripping drives should be created as another app.
# https://askubuntu.com/questions/147800/ripping-dvd-to-iso-accurately

#new way needs user to set the amount of makemkv instances allowed and if drives lock one each
#one thread does the watching and starts up the relevent tasks in another thread.
class Ripper:
    '''Main Class to create an instance of the plugin'''

    __running = False
    __available_drives = Hardware.disc_drives()
    __drives = []

    # __video_labeler = None
    # __converter = None
    # __renamer = None
    # __running = False

    @classproperty
    def running(cls):
        '''returns if ripper running'''
        return cls.__running

    @classproperty
    def enabled(cls):
        '''returns if ripper is enabled'''
        return CONFIG['ripper']['enabled'].value

    @classmethod
    def start(cls):
        '''Starts the ripper'''
        if cls.running or cls.enabled is False:
            return

        # Create folders
        for location in CONFIG['ripper']['locations']:
            File.mkdir(location.value)

        # Check/Create Database Tables
        Database.call(SQLTable(AUDIO_INFO_DB_INFO))
        Database.call(SQLTable(AUDIO_CONVERT_DB_INFO))
        Database.call(SQLTable(VIDEO_INFO_DB_INFO))
        Database.call(SQLTable(VIDEO_CONVERT_DB_INFO))

        if CONFIG['ripper']['drives']['enabled'].value:
            cls.__start_drives()

        # cls.__running = True

    @classmethod
    def __start_drives(cls):
        '''Starts the ripper drives'''
        for key in cls.__available_drives.keys():
            if config := CONFIG['ripper']['drives'].get(key):
                if config['enabled'].value:
                    if platform.system() == 'Linux':
                        cls.__drives.append(DriveLinux(config))

        # Start the threads
        for drive in cls.__drives:
            drive.start_thread()








    @classmethod
    def stop(cls):
        '''Stops the ripper'''
        if cls.__running:
            # Stop the drives
            for drive in cls.__drives:
                drive.stop_thread()
            cls.__running = False
