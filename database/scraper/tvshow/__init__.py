"""Library Base Table"""
from __future__ import annotations  # TODO drop this when we hit python 3.10

from peewee import BooleanField
from peewee import CharField
from peewee import DateField
from peewee import DoubleField
from peewee import IntegerField
from peewee import TextField

from database.scraper.base import ScraperBaseTable


class ScraperTVShow(ScraperBaseTable):
    """Library Base TV Show"""

    backdrop_path = TextField(null=True)
    first_air_date = DateField(formats=["%y-%m-%d"])
    homepage = TextField()
    in_production = BooleanField()
    last_air_date = DateField(formats=["%y-%m-%d"])
    # last_episode_to_air
    name = TextField()
    next_episode_to_air = TextField(null=True)
    number_of_episodes = IntegerField()
    number_of_seasons = IntegerField()
    original_language = CharField(max_length=2)
    original_name = TextField()
    overview = TextField()
    popularity = DoubleField()
    poster_path = TextField(null=True)
    status = TextField()
    tagline = TextField()
    type = TextField()
    vote_average = DoubleField()
    vote_count = IntegerField()

    @classmethod
    def from_data_dict(cls, data: dict) -> ScraperTVShow:
        """Generates the model from a dict"""
        tvshow = cls.get_or_create(id=data["id"])
        tvshow.backdrop_path = data.get("backdrop_path", None)
        tvshow.first_air_date = data["first_air_date"]
        tvshow.homepage = data["homepage"]
        tvshow.in_production = data["in_production"]
        tvshow.last_air_date = data["last_air_date"]
        tvshow.name = data["name"]
        tvshow.next_episode_to_air = data.get("next_episode_to_air", None)
        tvshow.number_of_episodes = data["number_of_episodes"]
        tvshow.number_of_seasons = data["number_of_seasons"]
        tvshow.original_language = data["original_language"]
        tvshow.original_name = data["original_name"]
        tvshow.overview = data["overview"]
        tvshow.popularity = data["popularity"]
        tvshow.poster_path = data.get("poster_path", None)
        tvshow.status = data["status"]
        tvshow.tagline = data["tagline"]
        tvshow.type = data["type"]
        tvshow.vote_average = data["vote_average"]
        tvshow.vote_count = data["vote_count"]
        tvshow.save()
        return tvshow
