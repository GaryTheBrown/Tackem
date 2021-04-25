"""Library Base Table"""
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
