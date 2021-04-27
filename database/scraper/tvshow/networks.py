"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.network import ScraperNetwork
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowNetworks(ScraperBaseTable):
    """Library Base TV Show Network"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="networks")
    network = ForeignKeyField(ScraperNetwork, backref="tvshows")
