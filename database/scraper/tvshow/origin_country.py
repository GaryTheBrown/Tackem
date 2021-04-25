"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.countries import ScraperCountries
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowOriginCountry(ScraperBaseTable):
    """Library Base TV Show Origin Country"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="origin_country")
    country = ForeignKeyField(ScraperCountries, ScraperCountries.iso_3166_1, "tvshows")
