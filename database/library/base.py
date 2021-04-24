"""Library Base Table"""
import time

from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import TextField

from database import TableBase
from database.library.file import LibraryFile


class LibraryBaseTable(TableBase):
    """Library Base Table"""

    def inttime():
        return int(time.time())

    id = IntegerField(primary_key=True)
    file = ForeignKeyField(LibraryFile, backref="link")


class LibraryBaseCompanies(TableBase):
    """Library Base Companies"""

    id = IntegerField(primary_key=True)
    logo_path = TextField()
    name = TextField()
    origin_country = TextField()


class LibraryBaseCompaniesFull(LibraryBaseCompanies):
    """Library Base Companies Full"""

    description = TextField()
    headquarters = TextField()
    homepage = TextField()
    parent_company = ForeignKeyField("self", null=True)
