"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.genre.tvshows import ScraperGenreTVShows
from database.scraper.tvshow import ScraperTVShow


class ScraperTVShowGenres(ScraperBaseTable):
    """Library Base Tv Show Genres"""

    tvshow = ForeignKeyField(ScraperTVShow, backref="genres")
    genre = ForeignKeyField(ScraperGenreTVShows, backref="tvshows")
