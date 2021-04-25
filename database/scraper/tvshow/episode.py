"""Library Base Table"""
from peewee import DateField
from peewee import DoubleField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import TextField

from database.scraper.base import ScraperBaseTable
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowEpisode(ScraperBaseTable):
    """Library Base TV Show Episode"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="episodes")
    season = ForeignKeyField(ScraperTVShow, backref="episodes")
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
