'''Base Library Controller'''
from typing import List
import threading
from abc import ABCMeta, abstractmethod
from pathlib import Path
from libs.sql import Database
from libs.sql.table import Table
from libs.config.list import ConfigList
from libraries.db.library_files import LIBRARY_FILES_DB_INFO

class LibraryBase(metaclass=ABCMeta):
    '''Base Library Class'''

    def __init__(self, library_type: str, config: ConfigList, table: Table):
        self._name = config.var_name
        self._library_type = library_type
        self._config = config

        self._thread_run = False
        self._thread = threading.Thread(target=self.run, args=())
        self._thread.setName("{} Library: {}".format(library_type.capitalize(), self._name))

        Database.sql().table_checks(self._thread.getName(), table)

    def start(self):
        '''start the Library'''
        if self._thread_run is False:
            self._thread_run = True
            self._thread.start()

    def stop(self):
        '''stops the Library'''
        if self._thread_run is True:
            self._thread_run = False

    @abstractmethod
    def run(self):
        '''threadded run'''

    def _scan_folder_base(self, extensions: List[str]):
        '''Scans the folder For New Files'''

        for path in Path(self._config['location'].value).rglob('*'):
            extension = path.parts[-1].split(".")[-1]
            if extension not in extensions:
                continue

            if Database.sql().table_has_row(
                    self._thread.name,
                    LIBRARY_FILES_DB_INFO.name(),
                    {
                        "folder": path.joinpath().replace(path.name, ""),
                        "filename": path.name
                    }
            ):
                continue

            Database.sql().insert(
                self._thread.name,
                LIBRARY_FILES_DB_INFO.name(),
                {
                    "folder": path.joinpath().replace(path.name, ""),
                    "filename": path.name,
                    "type": self._library_type.lower(),
                    "checksum": None,
                    "last_check": 0,
                    "from_system": None,
                    "from_id": None
                }
            )

            yield Database.sql().select(
                self._thread.name,
                LIBRARY_FILES_DB_INFO.name(),
                {
                    "folder": path.joinpath().replace(path.name, ""),
                    "filename": path.name
                }
            )[0]
