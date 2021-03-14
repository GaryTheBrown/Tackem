'''Ripper init'''
from libs.database.where import Where
from libs.database.messages.select import SQLSelect
from libs.ripper.video_converter import VideoConverter
from data import HOMEFOLDER
from libs.ripper.iso import ISORipper
from data.database.ripper import AUDIO_INFO_DB, VIDEO_CONVERT_DB, VIDEO_INFO_DB
from pathlib import Path
from data.config import CONFIG
from libs.classproperty import classproperty
from libs.database import Database
from libs.database.messages import SQLTable
from libs.file import File
from libs.hardware import Hardware
from libs.ripper.drive import Drive
from libs.database.table import Table
from typing import List
from libs.database import Database
from threading import BoundedSemaphore
from data.config import CONFIG

# TODO add the converter to the ripper system and get it working. then make it so you can edit the
# data while this happens. if no data exists at the end put it into the labeler holder otherwise
# auto send it to the library for processing where it goes.

# TODO need a way of the system checking if it needs to do any secondery convertion (audio stuff
# mainly)

# TODO at this point it should maybe convert all tracks if no info available but allow you
# to say what is what for it to then follow the config rules in what to copy and then delete
# any others. if its not input after the converter then wait in a hold till it knows what is
# what. so a labeler section now works after the convertor and it's just a holding section
# if in here then saving the track data will send it to the library

# TODO deal with the renamer (this may just be removed and changed to move to library as we can pass
# the info in for what it is and let the library worry about it's filename)

# TODO WWW all the systems back to life
# TODO Add in the video Labeler and renamer as well, then look at adding the Audio stuff

# TODO get the ripper html stuff moved into the www folder in a single file removing the html part
# functions for the new way. POSSABLY NEED TO CHANGE HOW THIS SHOWS SO POSSABLY NEEDS TO BE
# REWRITTEN BUT USE IT FOR REFERENCE AND TAKE THE LAYOUT ACROSS

# TODO a seperate system for ripping drives should be created as another app.
# https://askubuntu.com/questions/147800/ripping-dvd-to-iso-accurately


class Ripper:
    '''Main Class to create an instance of the plugin'''

    __running = False

    __drives: List[Drive] = []

    __iso_pool_sema: BoundedSemaphore = None
    __iso_threads: List[ISORipper] = []
    __iso_loaded: List[str] = []

    __video_converter_pool_sema: BoundedSemaphore = None
    __video_converter_threads: List[VideoConverter] = []
    __video_converter_loaded: List[int] = []

    # __video_labeler = None
    # __renamer = None

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
        cls.cleanup_dead_iso_threads()
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
        Database.call(SQLTable(VIDEO_INFO_DB))
        Database.call(SQLTable(VIDEO_CONVERT_DB))

        cls.setup_makemkv()
        if CONFIG['ripper']['drives']['enabled'].value:
            cls.__start_drives()

        if CONFIG['ripper']['iso']['enabled'].value:
            cls.__start_isos()

        if CONFIG['ripper']['converter']['enabled'].value:
            cls.__start_converters()

        cls.__running = True

    @classmethod
    def setup_makemkv(cls):
        '''sets up the makemkv config (needed due to app key)'''
        folder = f"{HOMEFOLDER}/.MakeMKV/"
        File.mkdir(folder)
        with open(f'{folder}settings.conf', "w") as file:
            file.write('app_DefaultSelectionString = "+sel:all"\n')
            file.write('app_DefaultOutputFileName = "{t:N2}"\n')
            file.write('app_ccextractor = "/usr/bin/ccextractor"\n')
            file.write(f'app_key = "' +
                       CONFIG['ripper']['makemkv']['key'].value + '"\n')
            file.write('dvd_MinimumTitleLength = "0"')

    @classmethod
    def __start_drives(cls):
        '''Starts the ripper drives'''
        for key in Hardware.disc_drives().keys():
            if config := CONFIG['ripper']['drives'].get(key):
                if config['enabled'].value:
                    cls.__drives.append(Drive(config))

        # Start the threads
        for drive in cls.__drives:
            drive.start_thread()

    @classmethod
    def __start_isos(cls):
        '''starts the ISO ripper system and checks the upload folders for isos to add'''
        cls.__iso_pool_sema = BoundedSemaphore(
            value=CONFIG['ripper']['iso']['threadcount'].value
        )

        # Check for Audio ISOs
        iso_path = File.location(
            CONFIG['ripper']['locations']['audioiso'].value)
        for path in Path(iso_path).rglob('*.iso'):
            filename = ("/"+"/".join(path.parts[1:])).replace(iso_path, "")
            cls.iso_add(filename, AUDIO_INFO_DB)

        # Check For Video ISOs
        iso_path = File.location(
            CONFIG['ripper']['locations']['videoiso'].value)
        for path in Path(iso_path).rglob('*.iso'):
            filename = ("/"+"/".join(path.parts[1:])).replace(iso_path, "")
            cls.iso_add(filename, VIDEO_INFO_DB)

    @classmethod
    def __start_converters(cls):
        '''starts the converter system and checks the DB for tasks to do'''
        cls.__video_converter_pool_sema = BoundedSemaphore(
            value=CONFIG['ripper']['converter']['threadcount'].value
        )

        msg = SQLSelect(VIDEO_CONVERT_DB)
        Database.call(msg)
        if isinstance(msg.return_data, dict):
            cls.video_converter_add(msg.return_data['id'])
        else:
            for item in msg.return_data:
                cls.video_converter_add(item['id'])

    @classmethod
    def stop(cls):
        '''Stops the ripper'''
        if not cls.__running:
            return

        # Stop the drives
        for drive in cls.__drives:
            drive.stop_thread()

        if isinstance(cls.__iso_pool_sema, BoundedSemaphore):
            cls.cleanup_dead_iso_threads()
            for thread in cls.__iso_threads:
                thread.stop_thread()
            cls.__iso_pool_sema = None
            cls.__iso_threads = []
            cls.__iso_loaded = []

        if isinstance(cls.__video_converter_pool_sema, BoundedSemaphore):

            for thread in cls.__video_converter_threads:
                thread.stop_thread()
            cls.__video_converter_pool_sema = None
            cls.__video_converter_threads = []
            cls.__video_converter_loaded = []
        cls.__running = False

    @classmethod
    def iso_add(cls, filename: str, table: Table) -> bool:
        '''Action for other systems to add iso mainly the upload side'''
        # TODO need to change the DB calls in here to read the other info and add thh full info here
        if not CONFIG['ripper']['iso']['enabled'].value:
            return False
        if filename in cls.__iso_loaded:
            return False
        cls.__iso_loaded.append(filename)
        cls.__iso_threads.append(
            ISORipper(cls.__iso_pool_sema, filename, table == VIDEO_INFO_DB)
        )
        return True

    @classmethod
    def cleanup_dead_iso_threads(cls):
        '''removes old threads from the list.'''
        if not CONFIG['ripper']['iso']['enabled'].value:
            return
        cls.__iso_threads = [t for t in cls.__iso_threads if t.thread_run]

    @classmethod
    def video_converter_add(cls, db_id: int) -> bool:
        '''Action for other systems to add a video converter task'''
        if not CONFIG['ripper']['converter']['enabled'].value:
            return False
        if db_id in cls.__video_converter_loaded:
            return False

        if Database.count(SQLSelect(VIDEO_CONVERT_DB, Where("id", db_id))) != 1:
            return False

        cls.__video_converter_loaded.append(db_id)
        cls.__video_converter_threads.append(
            VideoConverter(cls.__video_converter_pool_sema, db_id)
        )
        return True

    @classmethod
    def cleanup_dead_video_converter_threads(cls):
        '''removes old threads from the list.'''
        if not CONFIG['ripper']['converter']['enabled'].value:
            return
        cls.__video_converter_threads = [
            t for t in cls.__video_converter_threads if t.thread_run]
