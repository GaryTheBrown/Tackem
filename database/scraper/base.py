"""Library Base Table"""
from peewee import CharField
from peewee import DoubleField
from peewee import IntegerField
from peewee import TextField

from database import TableBase


class ScraperBaseTable(TableBase):
    """Library Base Table"""

    id = IntegerField(primary_key=True)


class ScraperBaseCast(ScraperBaseTable):
    """Library Base TV Show Cast"""

    gender = IntegerField(null=True)
    known_for_department = TextField()
    name = TextField()
    original_name = TextField()
    popularity = DoubleField()
    profile_path = TextField(null=True)
    character = TextField()
    credit_id = CharField(max_length=24)
    order = IntegerField()
