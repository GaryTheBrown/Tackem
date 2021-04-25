"""Libraries Root"""
from database.library.file import LibraryFile

# TODO Working on TVShow Data
# TODO Adding Cast Members Data for TV Shows and Movies
# TODO Add Scraper function to write data to the Library DB
# TODO possably move said function and the movie one to the library area
# TODO Get all tables loaded


class Libraries:
    """Libraries Root"""

    __checksum = None
    __movies = {}
    __tvshows = {}
    __music = {}
    __games = {}
    __loaded = False

    @classmethod
    def start(cls):
        """Start the library systems"""
        cls.__setup_tables()

    @classmethod
    def __setup_tables(cls):
        """function to deal with the database tables"""
        LibraryFile.table_setup()

    @classmethod
    def stop(cls):
        """Stop the library systems"""

    # def __init__(self):
    #     if self.__loaded:
    #         return

    #     LibraryFiles.table_setup()

    #     self.__checksum = FileChecker()

    #     config = CONFIG["libraries"]

    #     for movie_library in config["movies"]:
    #         self.__movies[movie_library.var_name] = MoviesLibrary(movie_library)

    #     # for tvshows_library in config['tvshows']:
    #     # for music_library in config['music']:
    #     # for games_library in config['games']:

    # def start(self):
    #     """Start the library systems"""
    #     self.__checksum.start()

    # def stop(self):
    #     """Stop the library systems"""
    #     self.__checksum.stop()
