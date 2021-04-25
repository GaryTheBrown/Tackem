"""Scraper Databases"""
from peewee import ForeignKeyField
from peewee import TextField

from database.scraper.base import ScraperBaseTable


class ScraperCompanies(ScraperBaseTable):
    """Library Base Companies"""

    logo_path = TextField()
    name = TextField()
    origin_country = TextField()
    description = TextField(null=True)
    headquarters = TextField(null=True)
    homepage = TextField(null=True)
    parent_company = ForeignKeyField("self", null=True)
