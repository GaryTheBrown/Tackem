"""Library Base Table"""
from peewee import ForeignKeyField
from peewee import IntegerField

from database.scraper.base import ScraperBaseCast
from database.scraper.movie import ScraperMovie


class ScraperMovieCast(ScraperBaseCast):
    """Library Base Movie Cast"""

    movie = ForeignKeyField(ScraperMovie, backref="cast")
    cast_id = IntegerField()
