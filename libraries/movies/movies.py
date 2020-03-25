'''Movie Libary Controller'''
from glob import glob
import threading
from libs.sql.column import Column


class MoviesLibrary():
    '''Movie Library Class'''

    _event_lock = threading.Event()
    _event_list = []
    _event_list_lock = threading.Lock()

    _thread_run = True

    _DB_VARIABLES = [
        Column("id", "integer", primary_key=True, not_null=True),
        Column("filename", "text", not_null=True),
        Column("added", "datetime", not_null=True,
               default="CURRENT_TIMESTAMP", default_raw=True),
        Column("imdb", "varchar(9)", default="NULL", default_raw=True)
    ]
    _DB_VERSION = 1

    def __init__(self, name, tackem_system):
        self._tackem_system = tackem_system
        self.name = name.split(" ")[-1]
        self._db_name = "movies_" + name.split(" ")[-1]

        self._thread = threading.Thread(target=self.run, args=())
        self._thread.setName("Movies Library:" + self.name)
        self._tackem_system.sql.table_check(self._thread.getName(),
                                            self._db_name,
                                            self._DB_VARIABLES,
                                            self._DB_VERSION)

    def scan_folder(self):
        '''Scans the folder For New Files'''
        glob_movie_list = glob(self._tackem_system.config()['location'] + "*")
        glob_movie_list.sort()
        for full_path_movie in glob_movie_list:
            movie = full_path_movie.replace(
                self._tackem_system.config()['location'], "")
            if self._tackem_system.sql.table_has_row(self._db_name, {"filename": movie}):
                continue
            print(movie + " Not in DB ADDING")

    def run(self):
        '''threadded run'''
        # inital run of information check
        self.scan_folder()

        while self._thread_run:
            if not self._thread_run:
                return
