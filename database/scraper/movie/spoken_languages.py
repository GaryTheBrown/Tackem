"""Library Base Table"""
from peewee import CharField
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.movie import ScraperMovie


class ScraperMovieSpokenLanguages(ScraperBaseTable):
    """Library Base Movie Spoken Languages"""

    movie = ForeignKeyField(ScraperMovie, backref="spoken_languages")
    iso_639_1 = CharField(max_length=2)
