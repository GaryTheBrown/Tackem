"""Library Base Table"""
from peewee import CharField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import TextField

from database.scraper.base import ScraperBaseTable
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowCreatedBy(ScraperBaseTable):
    """Library Base TV Show Created By"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="created_by")
    credit_id = CharField(max_length=24)
    name = TextField()
    gender = IntegerField(null=True)
    profile_path = TextField(null=True)
