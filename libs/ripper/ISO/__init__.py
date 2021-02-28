'''Root system for ISO Ripping using a Folder watcher'''
from libs.database.table import Table
from libs.database.messages.update import SQLUpdate
from libs.database.messages.insert import SQLInsert
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
from threading import BoundedSemaphore
from data.config import CONFIG
from data.database.ripper import AUDIO_INFO_DB, VIDEO_INFO_DB

class RipperISO:
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
        # cls.__audio_watcher = FolderWatcher(
        #     CONFIG['ripper']["locations"]["audioiso"].value,
        #     cls.__audio_file_detected,
        #     True,
        #     60
        # )

        # cls.__video_watcher = FolderWatcher(
        #     CONFIG['ripper']["locations"]["videoiso"].value,
        #     cls.__video_file_detected,
        #     True,
        #     60
        # )

    @classmethod
    def stop(cls):
        '''Stops the ripper ISO Watcher'''
        # cls.__audio_watcher.stop_thread()
        # cls.__video_watcher.stop_thread()

        #STOP any running makemkv systems here.
        cls.cleanup_dead_threads()
        for thread in cls.__threads:
            thread.stop_thread()

    @classmethod
    def file_add(cls, filename: str, table: Table):
        '''Action for other systems to add iso mainly the upload side'''
        if filename in cls.__loaded_files:
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

        cls.__loaded_files.append(filename)

        if platform.system() == 'Linux':
            cls.__threads.append(
                ISORipperLinux(msg.return_data, cls.__pool_sema)
            )



    @classmethod
    def __audio_file_detected(cls):
        '''action when a new audio ISO is detected'''
        cls.__file_detected(
            File.location(CONFIG['ripper']["locations"]["audioiso"].value),
            AUDIO_INFO_DB
        )

    @classmethod
    def __video_file_detected(cls):
        '''action when a new video ISO is detected'''
        cls.__temp_file_detected(
            File.location(CONFIG['ripper']["locations"]["videoiso"].value),
            VIDEO_INFO_DB
        )

    @classmethod
    def __file_detected(cls, iso_path: str, table: Table):
        '''action when a new audio ISO is detected'''
        for path in Path(iso_path).rglob('*.iso'):
            filename = ("/"+"/".join(path.parts[1:])).replace(iso_path, "")
            cls.file_add(filename, table)

    @classmethod
    def cleanup_dead_threads(cls):
        '''removes old threads from the list.'''
        cls.__threads = [t for t in cls.__threads if t.thread_run]
