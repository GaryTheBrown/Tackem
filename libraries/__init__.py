"""Library Master System"""
from database.library.file import LibraryFile
from database.library.movie import LibraryMovie
from libraries.file_checker import FileChecker


class Library:
    """Library Master System"""

    @classmethod
    def start(cls):
        """Start the library systems"""
        cls.__setup_tables()
        FileChecker.setup()
        FileChecker.start()

    @classmethod
    def __setup_tables(cls):
        """function to deal with the database tables"""
        LibraryFile.table_setup()
        LibraryMovie.table_setup()

    @classmethod
    def stop(cls):
        """Stop the library systems"""
        FileChecker.stop()
