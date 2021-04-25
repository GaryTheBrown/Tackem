"""Library Base Table"""
from peewee import ForeignKeyField
from peewee import IntegerField

from database.scraper.base import ScraperBaseTable
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowEpisodeRunTime(ScraperBaseTable):
    """Library Base TV Show Episode Run Time"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="episode_run_time")
    run_time = IntegerField()
