'''Ripper init'''
from libs.ripper.iso import ISORipper
from data.database.ripper import AUDIO_CONVERT_DB, AUDIO_INFO_DB
from data.database.ripper import VIDEO_CONVERT_DB, VIDEO_INFO_DB
import platform
from data.config import CONFIG
from libs.classproperty import classproperty
from libs.database import Database
from libs.database.messages import SQLTable
from libs.file import File
from libs.hardware import Hardware
from libs.ripper.drive import Drive
from libs.database.table import Table
from libs.database.messages.update import SQLUpdate
from libs.database.messages.insert import SQLInsert
from typing import List
from libs.database.where import Where
from libs.database import Database
from libs.database.messages import SQLSelect
from threading import BoundedSemaphore
from data.config import CONFIG


#TODO need to make a page for uploads and the API for the ripper to recieve the UUID, SHA256, LABEL and
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

    __iso_pool_sema: BoundedSemaphore = None

    __iso_threads: List[ISORipper] = []
    __loaded_isos: List[str] = []

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

    @classproperty
    def drives(cls) -> list:
        '''Returns the Enabled drives'''
        return cls.__drives

    @classproperty
    def isos(cls) -> List[ISORipper]:
        '''returns the iso threads'''
        cls.cleanup_dead_threads()
        return cls.__iso_threads

    @classmethod
    def start(cls):
        '''Starts the ripper'''
        if cls.running or cls.enabled is False:
            return

        # Create folders
        for location in CONFIG['ripper']['locations']:
            File.mkdir(location.value)

        # Check/Create Database Tables
        Database.call(SQLTable(AUDIO_INFO_DB))
        Database.call(SQLTable(AUDIO_CONVERT_DB))
        Database.call(SQLTable(VIDEO_INFO_DB))
        Database.call(SQLTable(VIDEO_CONVERT_DB))

        if CONFIG['ripper']['drives']['enabled'].value:
            cls.__start_drives()

        if CONFIG['ripper']['iso']['enabled'].value:
            cls.__start_drives()

        cls.__running = True

    @classmethod
    def __start_drives(cls):
        '''Starts the ripper drives'''
        for key in cls.__available_drives.keys():
            if config := CONFIG['ripper']['drives'].get(key):
                if config['enabled'].value:
                    cls.__drives.append(Drive(config))

        # Start the threads
        for drive in cls.__drives:
            drive.start_thread()

    @classmethod
    def __start_isos(cls):
        '''starts the ripper system and checks the upload folders for isos to add'''
        cls.__iso_pool_sema = BoundedSemaphore(value=CONFIG['ripper']['iso']['threadcount'].value)


    @classmethod
    def stop(cls):
        '''Stops the ripper'''
        if cls.__running:
            # Stop the drives
            for drive in cls.__drives:
                drive.stop_thread()

            if isinstance(cls.__iso_pool_sema, BoundedSemaphore):
                cls.cleanup_dead_threads()
                for thread in cls.__iso_threads:
                    thread.stop_thread()
                cls.__iso_pool_sema = None
                cls.__iso_threads = []
                cls.__loaded_isos = []
            cls.__running = False

    @classmethod
    def iso_add(cls, filename: str, table: Table):
        '''Action for other systems to add iso mainly the upload side'''
        if not CONFIG['ripper']['iso']['enabled'].value:
            return

        if filename in cls.__loaded_isos:
            return

        msg = SQLSelect(
            table,
            Where("iso_file", filename),
        )
        Database.call(msg)

        if isinstance(msg.return_data, dict):
            Database.call(
                SQLUpdate(
                    table,
                    Where(
                        "id",
                        msg.return_data['id']
                    ),
                    ripped=False,
                    ready_to_convert=False,
                    ready_to_rename=False,
                    ready_for_library=False,
                    completed=False
                )
            )
        else:
            Database.call(
                SQLInsert(
                    table,
                    iso_file=filename
                )
            )

        Database.call(msg)

        msg = SQLSelect(
            table,
            Where("iso_file", filename),
        )
        Database.call(msg)

        cls.__loaded_isos.append(filename)
        cls.__iso_threads.append(
            ISORipper(msg.return_data, cls.__iso_pool_sema)
        )

    @classmethod
    def cleanup_dead_threads(cls):
        '''removes old threads from the list.'''
        if not CONFIG['ripper']['iso']['enabled'].value:
            return
        cls.__iso_threads = [t for t in cls.__iso_threads if t.thread_run]
