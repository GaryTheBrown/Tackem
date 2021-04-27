"""Library Base Table"""
from __future__ import annotations  # TODO drop this when we hit python 3.10

from peewee import ForeignKeyField

from database.scraper.person import ScraperBaseCast
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowCast(ScraperBaseCast):
    """Library Base TV Show Cast"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="cast")

    @classmethod
    def from_data_dict(cls, data: dict, tv_show: ScraperTVShow) -> ScraperTVShowCast:
        """Generates the model from a dict"""
        cast = cls.get_or_create(id=data["id"])
        cast.tv_show = tv_show
        cast.gender = data["gender"]
        cast.known_for_department = data["known_for_department"]
        cast.name = data["name"]
        cast.original_name = data["original_name"]
        cast.popularity = data["popularity"]
        cast.profile_path = data["profile_path"]
        cast.character = data["character"]
        cast.credit_id = data["credit_id"]
        cast.order = data["order"]
        cast.save()
        return cast
