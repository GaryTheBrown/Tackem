"""Library Movies Table"""
from peewee import CharField
from peewee import ForeignKeyField

from database import Database
from database import SoftTableBase
from database import ThreadSafeDatabaseMetadata
from database.library.files import LibraryFiles


class LibraryMovies(SoftTableBase):
    """Library Movies Table"""

    fileid = ForeignKeyField(LibraryFiles, field="id", backref="file")
    imdb = CharField(max_length=9)

    class Meta:
        table_name = "library_movies"
        database = Database.db
        model_metadata_class = ThreadSafeDatabaseMetadata
