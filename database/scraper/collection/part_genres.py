"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.collection.part import ScraperCollectionPart
from database.scraper.genre.movies import ScraperGenreMovies


class ScraperCollectionPartGenres(ScraperBaseTable):
    """Library Base Collection Part Genres"""

    collection_part = ForeignKeyField(ScraperCollectionPart, backref="genres")
    genre = ForeignKeyField(ScraperGenreMovies)
