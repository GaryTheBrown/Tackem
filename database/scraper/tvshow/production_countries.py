"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.country import ScraperCountry
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowProductionCountries(ScraperBaseTable):
    """Library Base TVShow Production Countries"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="production_countries")
    country = ForeignKeyField(ScraperCountry, ScraperCountry.iso_3166_1, "tvshows")
