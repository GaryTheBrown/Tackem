"""Library Base Table"""
from __future__ import annotations  # TODO drop this when we hit python 3.10

from peewee import DateField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import TextField

from database.scraper.base import ScraperBaseTable
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowSeason(ScraperBaseTable):
    """Library Base TV Show Season"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="seasons")
    air_date = DateField(formats=["%y-%m-%d"])
    episode_count = IntegerField()
    name = TextField()
    overview = TextField()
    poster_path = TextField(null=True)
    season_number = IntegerField()

    @classmethod
    def from_data_dict(cls, data: dict, tvshow: ScraperTVShow) -> ScraperTVShowSeason:
        """Generates the model from a dict"""
        season = cls.get_or_create(id=data["id"])
        season.air_date = data["air_date"]
        season.episode_count = data["episode_count"]
        season.name = data["name"]
        season.overview = data["overview"]
        season.poster_path = data["poster_path"]
        season.season_number = data["season_number"]
        season.save()
        return season
