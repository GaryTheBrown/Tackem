"""Scraper Table"""
from peewee import ForeignKeyField

from database.scraper.base import ScraperBasePerson
from database.scraper.base import ScraperBaseTable
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowCreatedByPerson(ScraperBasePerson):
    """Scraper TV Show Created By Person"""


class ScraperTVShowCreatedBy(ScraperBaseTable):
    """Scraper TV Show Created By"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="created_by")
    creator = ForeignKeyField(ScraperBasePerson, backref="tvshows")
