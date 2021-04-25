"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper import ScraperGenreMovies
from database.scraper.base import ScraperBaseTable
from database.scraper.collection.part import ScraperCollectionPart


class ScraperCollectionPartGenres(ScraperBaseTable):
    """Library Base Collection Part Genres"""

    collection_part = ForeignKeyField(ScraperCollectionPart, backref="genres")
    genre = ForeignKeyField(ScraperGenreMovies)
