"""Scraper Databases"""
from peewee import TextField

from database import TableBase


class ScraperNetworks(TableBase):
    """Library Base Network"""

    headquarters = TextField(null=True)
    homepage = TextField(null=True)
    logo_path = TextField(null=True)
    name = TextField()
    origin_country = TextField()
