"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.company import ScraperCompany
from database.scraper.movie import ScraperMovie


class ScraperMovieProductionCompanies(ScraperBaseTable):
    """Library Base Movie Production Companies"""

    movie = ForeignKeyField(ScraperMovie, backref="production_companies")
    company = ForeignKeyField(ScraperCompany, backref="movies")
