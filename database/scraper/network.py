"""Scraper Databases"""
from __future__ import annotations  # TODO drop this when we hit python 3.10

from peewee import TextField

from database import TableBase


class ScraperNetwork(TableBase):
    """Library Base Network"""

    headquarters = TextField(null=True)
    homepage = TextField(null=True)
    logo_path = TextField(null=True)
    name = TextField()
    origin_country = TextField()

    @classmethod
    def from_data_dict(cls, data: dict) -> ScraperNetwork:
        """Generates the model from a dict"""
        return cls.get_or_create(
            id=data["id"],
            name=data["name"],
            logo_path=data["logo_path"],
            origin_country=data["origin_country"],
        )
