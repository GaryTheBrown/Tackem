'''Base Library Controller'''
from typing import Generator
import threading
from abc import ABCMeta, abstractmethod
from pathlib import Path
from watchdog.events import PatternMatchingEventHandler, FileSystemEvent
from watchdog.observers import Observer
from libs.database import Database
from libs.database.messages import SQLInsert, SQLSelect, SQLTable
from libs.database.table import Table
from libs.database.where import Where
from libs.config.list import ConfigList
from libraries.db.library_files import LIBRARY_FILES_DB_INFO
from data.config import CONFIG

class LibraryBase(metaclass=ABCMeta):
    '''Base Library Class'''

    TYPE_MOVIES = 1
    TYPE_TVSHOWS = 2
    TYPE_MUSIC = 3
    TYPE_GAMES = 4

    @classmethod
    def type_to_string(cls, library_type: int) -> str:
        '''change type int to string'''
        if library_type == cls.TYPE_MOVIES:
            return "Movies"
        if library_type == cls.TYPE_TVSHOWS:
            return "TVShows"
        if library_type == cls.TYPE_MUSIC:
            return "Music"
        if library_type == cls.TYPE_GAMES:
            return "Games"
        return "UNKNOWN"

    def __init__(self, library_type: int, config: ConfigList, table: Table):
        self._name = config.var_name
        self._library_type = library_type
        self._config = config
        self._file_types = "video"
        if self._library_type == self.TYPE_MUSIC:
            self._file_types = "audio"
        elif self._library_type == self.TYPE_GAMES:
            self._file_types = "game"

        self._thread_run = False
        self._thread = threading.Thread(target=self.run, args=())
        self._thread.setName(f"{LibraryBase.type_to_string(library_type)} Library: {self._name}")

        self.__folder_watcher = None
        self.__folder_observer = None

        Database.call(SQLTable(table))
        self.folder_watcher_setup()

    def folder_watcher_setup(self):
        '''Sections for setting up the folder watcher watchdog'''
        patterns = "*"
        ignore_patterns = ""
        ignore_directories = False
        case_sensitive = True
        self.__folder_watcher = PatternMatchingEventHandler(
            patterns,
            ignore_patterns,
            ignore_directories,
            case_sensitive)

        self.__folder_watcher.on_created = self._folder_on_created
        self.__folder_watcher.on_deleted = self._folder_on_deleted
        self.__folder_watcher.on_modified = self._folder_on_modified
        self.__folder_watcher.on_moved = self._folder_on_moved

        path = self._config['location'].value
        go_recursively = True
        self.__folder_observer = Observer()
        self.__folder_observer.schedule(self.__folder_watcher, path, recursive=go_recursively)


    def start(self):
        '''Start the library'''
        if self._thread_run is False:
            self._thread_run = True
            self._thread.start()
            self.__folder_observer.start()

    def stop(self):
        '''Stops the library'''
        if self._thread_run is True:
            self._thread_run = False
            self.__folder_observer.stop()
            self.__folder_observer.join()

    @abstractmethod
    def run(self):
        '''abstract Run Method'''

    def _scan_folder_base(self) -> Generator:
        '''Scans the folder for new files'''

        for path in Path(self._config['location'].value).rglob('*'):
            extension = path.parts[-1].split(".")[-1]
            if extension not in CONFIG['libraries']['global']['extensions'][self._file_types].value:
                continue

            msg1 = SQLSelect(
                LIBRARY_FILES_DB_INFO.name(),
                Where("folder", path.joinpath().replace(path.name, "")),
                Where("filename", path.name)
            )
            Database.call(msg1)

            if isinstance(msg1.return_data, dict):
                continue

            msg2 = SQLInsert(
                LIBRARY_FILES_DB_INFO.name(),
                folder=path.joinpath().replace(path.name, ""),
                filename=path.name,
                type=self._library_type.lower(),
                checksum=None,
                last_check=0,
                from_system=None,
                from_id=None
            )

            Database.call(msg2)

            msg3 = SQLSelect(
                LIBRARY_FILES_DB_INFO.name(),
                Where("folder", path.joinpath().replace(path.name, "")),
                Where("filename", path.name)
            )

            Database.call(msg3)

            yield msg3.return_data

    def _folder_on_created(self, event: FileSystemEvent):
        '''New file added to folder'''
        print(f"{event.src_path} has been created!")

    def _folder_on_deleted(self, event: FileSystemEvent):
        '''File was deleted from the folder'''
        print(f"deleted {event.src_path}!")

    def _folder_on_modified(self, event: FileSystemEvent):
        '''File has been Modified in the folder'''
        print(f"{event.src_path} has been modified")

    def _folder_on_moved(self, event: FileSystemEvent):
        '''File has been Moved in the folder'''
        print(f"moved {event.src_path} to {event.dest_path}")
