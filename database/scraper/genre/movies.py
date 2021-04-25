"""Scraper Databases"""
from peewee import IntegerField
from peewee import TextField

from database import TableBase


class ScraperGenreMovies(TableBase):
    """Library Base Genre Movies"""

    id = IntegerField(primary_key=True)
    name = TextField()
