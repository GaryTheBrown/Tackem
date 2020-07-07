'''Libraries Root'''
from config_data import CONFIG
from libs.sql.column import Column
from libs.sql import Database
from libraries.db.library_files import LIBRARY_FILES_DB_INFO
from libraries.checksum import FileChecker
from libraries.movies import MoviesLibrary

class Libraries:
    '''Libraries Root'''

    __checksum = None
    __movies = {}
    __tvshows = {}
    __music = {}
    __games = {}
    __loaded = False

    def __init__(self):
        if self.__loaded:
            return

        Database.sql().table_checks("Library Root", LIBRARY_FILES_DB_INFO)
        self.__checksum = FileChecker()

        config = CONFIG['libraries']

        for movie_library in config['movies']:
            self.__movies[movie_library.var_name] = MoviesLibrary(movie_library)

        # for tvshows_library in config['tvshows']:
        # for music_library in config['music']:
        # for games_library in config['games']:

    def start(self):
        '''Start the library systems'''
        self.__checksum.start()

    def stop(self):
        '''Stop the library systems'''
        self.__checksum.stop()

LIBRARIES = Libraries()
