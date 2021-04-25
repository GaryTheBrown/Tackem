"""Library Base Table"""
from peewee import BooleanField
from peewee import CharField
from peewee import DateField
from peewee import DoubleField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import TextField

from database.scraper.base import ScraperBaseTable
from database.scraper.collection import ScraperCollection


class ScraperMovie(ScraperBaseTable):
    """Library Base Movie"""

    backdrop_path = TextField(null=True)
    belongs_to_collection = ForeignKeyField(ScraperCollection, null=True)
    budget = IntegerField()
    homepage = TextField(null=True)
    imdb_id = CharField(max_length=9, null=True)
    original_language = TextField()
    original_title = TextField()
    overview = TextField(null=True)
    popularity = IntegerField()
    poster_path = TextField(null=True)
    release_date = DateField(formats=["%y-%m-%d"])
    revenue = IntegerField()
    runtime = IntegerField(null=True)
    status = CharField(max_length=15)
    tagline = TextField(null=True)
    title = TextField()
    video = BooleanField()
    vote_average = DoubleField()
    vote_count = IntegerField()
