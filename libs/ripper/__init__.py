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
from libs.ripper.drive.linux import DriveLinux

#TODO Working on the makemkv system so it can take input from drive or iso systems
#TODO Make the ISO section work/ finish off it's systems
# need to make a page for uploads and the API for the ripper to recieve the UUID, SHA256, LABEL and
# filename then give a key for upload back.

#TODO WWW all the systems back to life
#TODO Add in the video Labeler and renamer as well, then look at adding the Audio stuff


# TODO get the ripper html stuff moved into the www folder in a single file removing the html part
# functions for the new way. POSSABLY NEED TO CHANGE HOW THIS SHOWS SO POSSABLY NEEDS TO BE
# REWRITTEN BUT USE IT FOR REFERENCE AND TAKE THE LAYOUT ACROSS

# TODO add the option of ripping locally or just giving ISO, use the same evnet stuff thats in
# library to watch a folder for new files then start a iso ripper (using limits semphores)

# TODO get the converter back in.
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
        '''Returns if ripper running'''
        return cls.__running

    @classproperty
    def enabled(cls):
        '''Returns if ripper is enabled'''
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

        cls.__running = True

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

    @classproperty
    def drives(cls) -> list:
        '''Returns the Enabled drives'''
        return cls.__drives