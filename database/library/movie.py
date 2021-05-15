"""Library Movie"""
from peewee import CharField
from peewee import ForeignKeyField

from database import SoftTableBase
from database.library.file import LibraryFile
from database.scraper.movie import ScraperMovie
from database.user import User


class LibraryMovie(SoftTableBase):
    """Library Movie Database"""

    file = ForeignKeyField(LibraryFile)
    data = ForeignKeyField(ScraperMovie, backref="library_items")
    request_user = ForeignKeyField(User, backref="movies")
    quality = CharField(max_length=32)
