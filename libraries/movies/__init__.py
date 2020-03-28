'''Library Movies Controller'''
from glob import glob
import threading
from libs.sql.column import Column
from libs.sql import Database
from libs.config.list import ConfigList
from libraries.library_base import LibraryBase
from libraries.db.movies import LIBRARY_MOVIE_DB_INFO

class MoviesLibrary(LibraryBase):
    '''Library Movies Controller'''

    def __init__(self, name: str, config: ConfigList):
        super().__init__(name, "movies", config)

        self._event_lock = threading.Event()
        self._event_list = []
        self._event_list_lock = threading.Lock()

        self.__thread = threading.Thread(target=self.run, args=())
        self.__thread.setName("Movies Library:" + name)
        Database.sql().table_checks(
            self.__thread.getName(),
            LIBRARY_MOVIE_DB_INFO,
            [name]
        )

    def scan_folder(self):
        '''Scans the folder For New Files'''
        glob_movie_list = glob(self._config['location'].value + "*")
        glob_movie_list.sort()
        for full_path_movie in glob_movie_list:
            movie = full_path_movie.replace(
                self._config['location'].value,
                ""
            )
            if Database.sql().table_has_row(
                    LIBRARY_MOVIE_DB_INFO['name'].format(self._name),
                    {
                        "filename": movie
                    }
            ):
                continue
            print(movie + " Not in DB ADDING")

    def run(self):
        '''threadded run'''
        # inital run of information check
        self.scan_folder()

        while self._thread_run:
            if not self._thread_run:
                return
