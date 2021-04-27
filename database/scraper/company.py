"""Scraper Databases"""
from __future__ import annotations  # TODO drop this when we hit python 3.10

from peewee import ForeignKeyField
from peewee import TextField

from database.scraper.base import ScraperBaseTable


class ScraperCompany(ScraperBaseTable):
    """Library Base Companies"""

    logo_path = TextField()
    name = TextField()
    origin_country = TextField()
    description = TextField(null=True)
    headquarters = TextField(null=True)
    homepage = TextField(null=True)
    parent_company = ForeignKeyField("self", null=True)

    @classmethod
    def from_data_dict(cls, data: dict) -> ScraperCompany:
        """Generates the model from a dict"""
        return cls.get_or_create(
            id=data["id"],
            logo_path=data["logo_path"],
            name=data["name"],
            origin_country=data["origin_country"],
        )
