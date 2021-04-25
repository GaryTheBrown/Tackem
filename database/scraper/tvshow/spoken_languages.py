"""Library Base Table"""
from peewee import CharField
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowSpokenLanguages(ScraperBaseTable):
    """Library Base TV Show Spoken Languages"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="spoken_languages")
    iso_639_1 = CharField(max_length=2)
