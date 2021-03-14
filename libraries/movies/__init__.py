"""Library Movies Controller"""
from libs.config.list import ConfigList
from libraries.library_base import LibraryBase
from data.database.library import LIBRARY_MOVIES_DB


class MoviesLibrary(LibraryBase):
    """Library Movies Controller"""

    def __init__(self, config: ConfigList):
        super().__init__(self.TYPE_MOVIES, config, LIBRARY_MOVIES_DB)

    def scan_folder(self):
        """Scans the folder For New Files"""
        for file in self._scan_folder_base():
            # add file info to LIBRARY_MOVIES_DB.name(self._name)
            print(f"DB FILE ADDED {file}")

    def run(self):
        """threadded run"""
        # inital run of information check
        while self._thread_run:
            if not self._thread_run:
                return
