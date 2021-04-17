"""Library Movies Table"""
from peewee import CharField
from peewee import ForeignKeyField

from data.database.library_files import LibraryFiles
from libs.database import Database
from libs.database import SoftTableBase
from libs.database import ThreadSafeDatabaseMetadata


class LibraryMovies(SoftTableBase):
    """Library Movies Table"""

    fileid = ForeignKeyField(LibraryFiles, field="id", backref="file")
    imdb = CharField(max_length=9)

    class Meta:
        table_name = "library_movies"
        database = Database.db
        model_metadata_class = ThreadSafeDatabaseMetadata
