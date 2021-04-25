"""Library Base Table"""
from peewee import BooleanField
from peewee import DateField
from peewee import DoubleField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import TextField

from database.scraper.base import ScraperBaseTable
from database.scraper.collection.part_genres import ScraperCollection


class ScraperCollectionPart(ScraperBaseTable):
    """Library Base Collection Part"""

    collection = ForeignKeyField(ScraperCollection, backref="parts")
    backdrop_path = TextField(null=True)
    original_language = TextField()
    original_title = TextField()
    overview = TextField()
    release_date = DateField(formats=["%y-%m-%d"])
    poster_path = TextField()
    popularity = DoubleField()
    title = TextField()
    video = BooleanField()
    vote_average = DoubleField()
    vote_count = IntegerField()
