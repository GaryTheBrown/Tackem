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
        Column("added", "datetime", not_null=True, default="CURRENT_TIMESTAMP", default_raw=True),
        Column("imdb", "varchar(9)", default="NULL", default_raw=True)
    ]
    _DB_VERSION = 2

    def __init__(self, name, config, db):
        self._config = config
        self.name = name
        self._db = db

        self._thread = threading.Thread(target=self.run, args=())
        self._thread.setName("Movies Library:" + self.name)
        print(self._thread.getName())

        db.table_check(self._thread.getName(),
                       name,
                       self._DB_VARIABLES,
                       self._DB_VERSION)

    def scan_folder(self):
        '''Scans the folder For New Files'''
        glob_movie_list = glob(self._config['location'] + "*")
        glob_movie_list.sort()
        for full_path_movie in glob_movie_list:
            movie = full_path_movie.replace(self._config['location'], "")
            if self._db.table_has_row(self.name, {"filename":movie}):
                continue
            print(movie + " Not in DB ADDING")


    def run(self):
        '''threadded run'''
        #inital run of information check
        self.scan_folder()

        # while self._thread_run:
        #     if not self._thread_run:
        #         return
