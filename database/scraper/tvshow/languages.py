"""Library Base Table"""
from peewee import CharField
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowLanguages(ScraperBaseTable):
    """Library Base TV Show Spoken Languages"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="languages")
    language = CharField(max_length=2)
