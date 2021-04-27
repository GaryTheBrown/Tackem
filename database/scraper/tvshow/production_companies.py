"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.company import ScraperCompany
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowProductionCompanies(ScraperBaseTable):
    """Library Base TVShow Production Companies"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="production_companies")
    company = ForeignKeyField(ScraperCompany, backref="tvshows")
