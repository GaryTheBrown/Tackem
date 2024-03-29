"""Ripper init"""
from pathlib import Path
from threading import BoundedSemaphore
from threading import Thread
from typing import List

from config import CONFIG
from data import HOMEFOLDER
from database.ripper.audio_info import RipperAudioInfo
from database.ripper.video_convert import RipperVideoConvertInfo
from database.ripper.video_info import RipperVideoInfo
from libs import classproperty
from libs.file import File
from libs.hardware import Hardware
from ripper.drive import Drive
from ripper.events import RipperEventMaster
from ripper.iso import ISORipper
from ripper.video_converter import VideoConverter

# TODO make it detect if the video is there for viewing and if so somehow allow it to be watched in
# the browser if possible

# TODO auto send it to the library for processing where it goes. Functions need to be in the library
# side and be agnostic so upload can accept files too. Do i want to have a DB table to put it in to
# hold this information so the library knows what to sort and once the file is copied over it checks
# if the file was copied correctly (compares them?) it then removes it from source and the DB

# TODO deal with the renamer (this may just be removed and changed to move to library as we can pass
# the info in for what it is and let the library worry about it's filename)

# TODO a seperate system for ripping drives should be created as another app.
# https://askubuntu.com/questions/147800/ripping-dvd-to-iso-accurately

# TODO add in Audio CD to this system

# TODO look at pytranscoder and see if it can be used to "preview" video files as well as replacing
# the video converter stuff
# https://github.com/mlsmithjr/transcoder
# https://pytranscoder.readthedocs.io/en/latest/

# https://stackoverflow.com/questions/3639604/html5-audio-video-and-live-transcoding-with-ffmpeg
# https://videojs.com/city
# https://blog.miguelgrinberg.com/post/video-streaming-with-flask/page/3
# https://docs.cherrypy.org/en/3.3.0/progguide/streaming.html


class Ripper:
    """Main Class to create an instance of the plugin"""

    __running = False

    __event_system: Thread = None

    __drives: List[Drive] = []

    __iso_pool_sema_count: int = 0
    __iso_pool_sema: BoundedSemaphore = None
    __iso_threads: List[ISORipper] = []

    __video_converter_pool_sema_count: int = 0
    __video_converter_pool_sema: BoundedSemaphore = None
    __video_converter_threads: List[VideoConverter] = []

    @classproperty
    def running(cls):
        """Returns if ripper running"""
        return cls.__running

    @classproperty
    def enabled(cls):
        """Returns if ripper is enabled"""
        return CONFIG["ripper"]["enabled"].value

    @classproperty
    def drives(cls) -> list:
        """Returns the Enabled drives"""
        return cls.__drives

    @classproperty
    def isos(cls) -> List[ISORipper]:
        """returns the iso threads"""
        cls.__cleanup_dead_iso_threads()
        return cls.__iso_threads

    @classproperty
    def maxisos(cls) -> int:
        """returns the max threads for isos"""
        return cls.__iso_pool_sema_count

    @classproperty
    def maxvideoconverters(cls) -> int:
        """returns the max threads for video converters"""
        return cls.__video_converter_pool_sema_count

    @classproperty
    def video_converters(cls) -> List[VideoConverter]:
        """returns the Video Converters threads"""
        cls.__cleanup_dead_video_converter_threads()
        return cls.__video_converter_threads

    @classmethod
    def start(cls):
        """Starts the ripper"""
        if cls.running or cls.enabled is False:
            return

        # Create folders
        for location in CONFIG["ripper"]["locations"]:
            File.mkdir(location.value)

        # Check/Create Database Tables
        RipperAudioInfo.table_setup()
        RipperVideoConvertInfo.table_setup()
        RipperVideoInfo.table_setup()

        cls.__running = True
        cls.__event_system = Thread(target=cls.__event_system_run, args=())
        cls.__event_system.start()

        cls.__setup_makemkv()
        if CONFIG["ripper"]["drives"]["enabled"].value:
            cls.__start_drives()

        if CONFIG["ripper"]["iso"]["enabled"].value:
            cls.__start_isos()

        if CONFIG["ripper"]["converter"]["enabled"].value:
            cls.__start_converters()

    @staticmethod
    def __setup_makemkv():
        """sets up the makemkv config (needed due to app key)"""
        folder = f"{HOMEFOLDER}/.MakeMKV/"
        File.mkdir(folder)
        with open(f"{folder}settings.conf", "w") as file:
            file.write('app_DefaultSelectionString = "+sel:all"\n')
            file.write('app_DefaultOutputFileName = "{t:N2}"\n')
            file.write('app_ccextractor = "/usr/bin/ccextractor"\n')
            file.write('app_key = "' + CONFIG["ripper"]["makemkv"]["key"].value + '"\n')
            file.write('dvd_MinimumTitleLength = "0"')

    @classmethod
    def __start_drives(cls):
        """Starts the ripper drives"""
        for key in Hardware.disc_drives().keys():
            if config := CONFIG["ripper"]["drives"].get(key):
                if config["enabled"].value:
                    cls.__drives.append(Drive(config))

        # Start the threads
        for drive in cls.__drives:
            drive.start_thread()

    @classmethod
    def __start_isos(cls):
        """starts the ISO ripper system and checks the upload folders for isos to add"""
        cls.__iso_pool_sema_count = CONFIG["ripper"]["iso"]["threadcount"].value
        cls.__iso_pool_sema = BoundedSemaphore(value=cls.__iso_pool_sema_count)

        # Check for ISOs
        iso_path = File.location(CONFIG["ripper"]["locations"]["iso"].value)
        for path in Path(iso_path).rglob("*.iso"):
            filename = ("/" + "/".join(path.parts[1:])).replace(iso_path, "")
            cls.iso_add(filename)

    @classmethod
    def __start_converters(cls):
        """starts the converter system and checks the DB for tasks to do"""
        cls.__video_converter_pool_sema_count = CONFIG["ripper"]["converter"]["threadcount"].value
        cls.__video_converter_pool_sema = BoundedSemaphore(
            value=cls.__video_converter_pool_sema_count
        )
        for item in RipperVideoConvertInfo.do_select():
            cls.video_converter_add_single(item.id)

    @classmethod
    def stop(cls):
        """Stops the ripper"""
        if not cls.__running:
            return

        cls.__running = False
        RipperEventMaster.stop()
        cls.__event_system.join()

        # Stop the drives
        for drive in cls.__drives:
            drive.stop_thread()

        if isinstance(cls.__iso_pool_sema, BoundedSemaphore):
            cls.__cleanup_dead_iso_threads()
            for thread in cls.__iso_threads:
                thread.stop_thread()
            cls.__iso_pool_sema = None
            cls.__iso_threads = []

        if isinstance(cls.__video_converter_pool_sema, BoundedSemaphore):
            cls.__cleanup_dead_video_converter_threads()
            for thread in cls.__video_converter_threads:
                thread.stop_thread()
            cls.__video_converter_pool_sema = None
            cls.__video_converter_threads = []

    @classmethod
    def iso_add(cls, filename: str) -> bool:
        """Action for other systems to add iso mainly the upload side"""
        if not CONFIG["ripper"]["iso"]["enabled"].value:
            return False

        cls.__cleanup_dead_iso_threads()
        for thread in cls.__iso_threads:
            if thread.filename == filename:
                return False

        cls.__iso_threads.append(ISORipper(cls.__iso_pool_sema, filename))
        return True

    @classmethod
    def __cleanup_dead_iso_threads(cls):
        """removes old threads from the list."""
        if not CONFIG["ripper"]["iso"]["enabled"].value:
            return
        cls.__iso_threads = [t for t in cls.__iso_threads if t.thread_run]

    @classmethod
    def video_converter_add_single(cls, db_id: int) -> bool:
        """Action for other systems to add a single video converter task"""
        if not CONFIG["ripper"]["converter"]["enabled"].value:
            return False

        cls.__cleanup_dead_video_converter_threads()
        for thread in cls.__video_converter_threads:
            if thread.db_id == db_id:
                return False

        if (
            RipperVideoConvertInfo.do_select().where(RipperVideoConvertInfo.id == db_id).count()
            != 1
        ):
            return False

        cls.__video_converter_threads.append(VideoConverter(cls.__video_converter_pool_sema, db_id))
        return True

    @classmethod
    def __cleanup_dead_video_converter_threads(cls):
        """removes old threads from the list."""
        if not CONFIG["ripper"]["converter"]["enabled"].value:
            return
        cls.__video_converter_threads = [t for t in cls.__video_converter_threads if t.thread_run]

    @classmethod
    def __event_system_run(cls):
        """system for allowing messages to be passed to the root of the ripper"""
        while cls.__running:
            event = RipperEventMaster.wait_and_get_event()
            if not cls.__running:
                return
            func = getattr(cls, event[0], None)
            if func and callable(func):
                func(*event[1])
