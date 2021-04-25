"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.countries import ScraperCountries
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowProductionCountries(ScraperBaseTable):
    """Library Base TVShow Production Countries"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="production_countries")
    country = ForeignKeyField(ScraperCountries, ScraperCountries.iso_3166_1, "tvshows")
