"""Scraper Table"""
from peewee import CharField
from peewee import DoubleField
from peewee import IntegerField
from peewee import TextField

from database.scraper.base import ScraperBaseTable


class ScraperBasePerson(ScraperBaseTable):
    """Scraper Person"""

    credit_id = CharField(max_length=24)
    name = TextField()
    gender = IntegerField(null=True)
    profile_path = TextField(null=True)


class ScraperBaseCast(ScraperBasePerson):
    """Scraper Cast"""

    known_for_department = TextField()
    original_name = TextField()
    popularity = DoubleField()
    character = TextField()
    order = IntegerField()
