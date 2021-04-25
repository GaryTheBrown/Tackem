"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.base import ScraperBaseTable
from database.scraper.genre.movies import ScraperGenreMovies
from database.scraper.movie import ScraperMovie


class ScraperMovieGenres(ScraperBaseTable):
    """Library Base Movie Genres"""

    movie = ForeignKeyField(ScraperMovie, backref="genres")
    genre = ForeignKeyField(ScraperGenreMovies)
