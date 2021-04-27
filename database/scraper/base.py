"""Scraper Table"""
from peewee import IntegerField

from database import TableBase


class ScraperBaseTable(TableBase):
    """Scraper Table"""

    id = IntegerField(primary_key=True)
