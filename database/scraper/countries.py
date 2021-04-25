"""Scraper Databases"""
from peewee import CharField
from peewee import TextField

from database import TableBase


class ScraperCountries(TableBase):
    """Library Base Countries"""

    iso_3166_1 = CharField(max_length=2)
    english_name = TextField()
    native_name = TextField()
