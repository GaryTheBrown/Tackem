'''Library Movies Controller'''
from glob import glob
from libs.sql.column import Column
from libs.sql import Database
from libs.config.list import ConfigList
from libraries.library_base import LibraryBase
from libraries.db.movie_base import LIBRARY_MOVIES_DB_INFO

class MoviesLibrary(LibraryBase):
    '''Library Movies Controller'''

    def __init__(self, config: ConfigList):
        super().__init__(self.TYPE_MOVIES, config, LIBRARY_MOVIES_DB_INFO)

    def scan_folder(self):
        '''Scans the folder For New Files'''
        for file in self._scan_folder_base():
            #add file info to LIBRARY_MOVIES_DB_INFO.name(self._name)
            print(f"DB FILE ADDED {file}")

    def run(self):
        '''threadded run'''
        # inital run of information check
        while self._thread_run:
            if not self._thread_run:
                return
