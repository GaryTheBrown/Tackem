"""Library Base Table"""
from __future__ import annotations  # TODO drop this when we hit python 3.10

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
    belongs_to_collection = ForeignKeyField(ScraperCollection, backref="movies", null=True)
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

    @classmethod
    def from_data_dict(cls, data: dict) -> ScraperMovie:
        """Generates the model from a dict"""
        movie = cls.get_or_create(id=data["id"])
        movie.backdrop_path = data.get("backdrop_path", None)
        movie.budget = data["budget"]
        movie.homepage = data.get("homepage", None)
        movie.imdb_id = data.get("imdb_id", None)
        movie.original_language = data["original_language"]
        movie.original_title = data["original_title"]
        movie.overview = data.get("overview", None)
        movie.popularity = data["popularity"]
        movie.poster_path = data.get("poster_path", None)
        movie.release_date = data["release_date"]
        movie.revenue = data["revenue"]
        movie.runtime = data.get("runtime", None)
        movie.status = data["status"]
        movie.tagline = data.get("tagline", None)
        movie.title = data["title"]
        movie.video = data["video"]
        movie.vote_average = data["vote_average"]
        movie.vote_count = data["vote_count"]
        movie.save()
        return movie
