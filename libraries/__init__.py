'''Libraries Root'''
from config_data import CONFIG
from libs.database.column import Column
from libs.database import Database
from libs.database.sql_message import SQLMessage
from libraries.db.library_files import LIBRARY_FILES_DB_INFO
from libraries.file_checker import FileChecker
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

        Database.call(SQLMessage(LIBRARY_FILES_DB_INFO))

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
