"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseCast
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowCast(ScraperBaseCast):
    """Library Base TV Show Cast"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="cast")
