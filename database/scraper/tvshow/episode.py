"""Library Base Table"""
from __future__ import annotations

from peewee import DateField
from peewee import DoubleField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import TextField

from database.scraper.base import ScraperBaseTable
from database.scraper.tvshow import ScraperTVShow
from database.scraper.tvshow.season import (
    ScraperTVShowSeason,
)  # TODO drop this when we hit python 3.10


class ScraperTVShowEpisode(ScraperBaseTable):
    """Library Base TV Show Episode"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="episodes")
    season = ForeignKeyField(ScraperTVShowSeason, backref="episodes")
    air_date = DateField(formats=["%y-%m-%d"])
    # crew
    episode_number = IntegerField()
    # guest_stars
    name = TextField()
    overview = TextField()
    production_code = TextField(null=True)
    season_number = IntegerField()
    still_path = TextField(null=True)
    vote_average = DoubleField()
    vote_count = IntegerField()

    @classmethod
    def from_data_dict(cls, data: dict, season: ScraperTVShowSeason) -> ScraperTVShowEpisode:
        """Generates the model from a dict"""
        episode = cls.get_or_create(id=data["id"])
        episode.tvshow = season.tvshow
        episode.season = season
        episode.air_date = data["air_date"]
        episode.episode_number = data["episode_number"]
        episode.name = data["name"]
        episode.overview = data["overview"]
        episode.production_code = data.get("production_code", None)
        episode.season_number = data["season_number"]
        episode.still_path = data.get("still_path", None)
        episode.vote_average = data["vote_average"]
        episode.vote_count = data["vote_count"]
        episode.save()
        return episode
