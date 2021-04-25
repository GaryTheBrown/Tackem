"""Library Base Table"""
from peewee import TextField

from database.scraper.base import ScraperBaseTable


class ScraperCollection(ScraperBaseTable):
    """Library Base Collection"""

    name = TextField()
    overview = TextField()
    poster_path = TextField(null=True)
    backdrop_path = TextField()
    overview = TextField(null=True)
