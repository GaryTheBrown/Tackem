'''Root system for ISO Ripping using a Folder watcher'''
from libs.ripper.ISO.linux import ISORipperLinux
import platform
from libs.file import File
from pathlib import Path
from typing import List
from libs.ripper.ISO.iso import ISORipper
from libs.database.where import Where
from libs.database import Database
from libs.database.messages import SQLSelect
from libs.watcher import FolderWatcher
import os
import time
from threading import BoundedSemaphore
from data.config import CONFIG
from data.database.ripper import AUDIO_INFO_DB_INFO, VIDEO_INFO_DB_INFO

class ISO:
    '''Root system for ISO Ripping using a Folder watcher'''

    __pool_sema: BoundedSemaphore = None
    __audio_watcher: FolderWatcher = None
    __video_watcher: FolderWatcher = None
    __threads: List[ISORipper] = []
    __loaded_files: List[str] = []
    @classmethod
    def start(cls):
        '''Starts the ripper ISO Watcher'''
        cls.__pool_sema = BoundedSemaphore(value=CONFIG['ripper']['iso']['threadcount'].value)
        audio_path = CONFIG['ripper']["locations"]["audioiso"].value
        video_path = CONFIG['ripper']["locations"]["videoiso"].value
        cls.__audio_watcher = FolderWatcher(audio_path, cls.__audio_file_detected, True, 60)
        cls.__video_watcher = FolderWatcher(video_path, cls.__video_file_detected, True, 60)


    @classmethod
    def stop(cls):
        '''Stops the ripper ISO Watcher'''
        cls.__audio_watcher.stop_thread()
        cls.__video_watcher.stop_thread()

        #STOP any running makemkv systems here.
        cls.cleanup_dead_threads()
        for thread in cls.__threads:
            thread.stop_thread()

    @classmethod
    def __audio_file_detected(cls):
        '''action when a new audio ISO is detected'''
        cls.__file_detected(
            File.location(CONFIG['ripper']["locations"]["audioiso"].value),
            AUDIO_INFO_DB_INFO.name()
        )

    @classmethod
    def __video_file_detected(cls):
        '''action when a new video ISO is detected'''
        cls.__file_detected(
            File.location(CONFIG['ripper']["locations"]["videoiso"].value),
            VIDEO_INFO_DB_INFO.name()
        )

    @classmethod
    def __file_detected(cls, iso_path: str, table_name: str):
        '''action when a new audio ISO is detected'''
        cls.wait_for_file_copy_complete()
        for path in Path(iso_path).rglob('*.iso'):
            filename = ("/"+"/".join(path.parts[1:])).replace(iso_path, "")
            msg = SQLSelect(
                table_name,
                Where("iso_file", filename),
                Where("ripped", False)
            )
            Database.call(msg)

            if not isinstance(msg.return_data, dict):
                continue

            if filename in cls.__loaded_files:
                continue

            cls.__loaded_files.append(filename)

            if platform.system() == 'Linux':
                cls.__threads.append(
                    ISORipperLinux(msg.return_data, cls.__pool_sema)
                )

    @classmethod
    def wait_for_file_copy_complete(cls, filename: str) -> bool:
        '''watches the file size until it stops'''
        historicalSize = -1
        while (historicalSize != os.path.getsize(filename)):
            historicalSize = os.path.getsize(filename)
            time.sleep(1)

    @classmethod
    def cleanup_dead_threads(cls):
        '''removes old threads from the list.'''
        cls.__threads = [t for t in cls.__threads if t.thread_run]
