"""Scraper Databases"""
from peewee import IntegerField
from peewee import TextField

from database import TableBase


class ScraperGenreTVShows(TableBase):
    """Library Base Genre TVShow"""

    id = IntegerField(primary_key=True)
    name = TextField()
