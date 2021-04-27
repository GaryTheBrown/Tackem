"""Library Base Table"""
from __future__ import annotations  # TODO drop this when we hit python 3.10

from peewee import TextField

from database.scraper.base import ScraperBaseTable


class ScraperCollection(ScraperBaseTable):
    """Library Base Collection"""

    name = TextField()
    overview = TextField()
    poster_path = TextField(null=True)
    backdrop_path = TextField()
    overview = TextField(null=True)

    @classmethod
    def from_data_dict(cls, data: dict) -> ScraperCollection:
        """Generates the model from a dict"""
        collection = cls.get_or_create(id=data["id"])
        collection.name = data["name"]
        collection.poster_path = data["poster_path"]
        collection.backdrop_path = data["backdrop_path"]
        collection.save()
        return collection
