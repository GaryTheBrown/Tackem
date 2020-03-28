'''Libraries Root'''
from config_data import CONFIG
from libs.sql.column import Column
from libs.sql import Database
from libraries.db.library_files import LIBRARY_FILES_DB_INFO

class Libraries:
    '''Libraries Root'''

    __movies = {}
    __tvshows = {}
    __games = {}
    __loaded = False

    def __init__(self):
        if self.__loaded:
            return

        Database.sql().table_checks("Library Root", LIBRARY_FILES_DB_INFO)

        config = CONFIG['libraries']

        #config['movies']
        #config['tvshows']
        #config['games']
        #config['music']


LIBRARIES = Libraries()
