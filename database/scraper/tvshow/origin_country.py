"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.country import ScraperCountry
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowOriginCountry(ScraperBaseTable):
    """Library Base TV Show Origin Country"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="origin_country")
    country = ForeignKeyField(ScraperCountry, ScraperCountry.iso_3166_1, "tvshows")
