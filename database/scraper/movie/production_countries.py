"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.country import ScraperCountry
from database.scraper.movie import ScraperMovie


class ScraperMovieProductionCountries(ScraperBaseTable):
    """Library Base Movie Production Countries"""

    movie = ForeignKeyField(ScraperMovie, backref="production_countries")
    country = ForeignKeyField(ScraperCountry, ScraperCountry.iso_3166_1, "movies")
