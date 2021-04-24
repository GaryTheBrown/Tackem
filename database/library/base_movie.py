"""Library Base Table"""
from peewee import BooleanField
from peewee import CharField
from peewee import DateField
from peewee import DoubleField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import TextField

from database import TableBase
from database.library.base import LibraryBaseCompanies
from database.library.base import LibraryBaseTable
from database.scraper import ScraperCountries
from database.scraper import ScraperGenreMovies


class LibraryBaseCollection(TableBase):
    """Library Base Collection"""

    id = IntegerField(primary_key=True)
    name = TextField()
    overview = TextField()
    poster_path = TextField(null=True)
    backdrop_path = TextField()


class LibraryBaseCollectionFull(LibraryBaseCollection):
    """Library Base Collection Full"""

    overview = TextField()


class LibraryBaseCollectionPart(TableBase):
    """Library Base Collection Part"""

    collection = ForeignKeyField(LibraryBaseCollectionFull, backref="parts")
    backdrop_path = TextField(null=True)
    original_language = TextField()
    original_title = TextField()
    overview = TextField()
    release_date = DateField(formats=["%y-%m-%d"])
    poster_path = TextField()
    popularity = DoubleField()
    title = TextField()
    video = BooleanField()
    vote_average = DoubleField()
    vote_count = IntegerField()


class LibraryBaseCollectionpartGenres(TableBase):
    """Library Base Movie Genres"""

    collection_part = ForeignKeyField(LibraryBaseCollectionPart, backref="genres")
    genre = ForeignKeyField(ScraperGenreMovies)


class LibraryBaseMovie(LibraryBaseTable):
    """Library Base Movie"""

    backdrop_path = TextField(null=True)
    belongs_to_collection = ForeignKeyField(LibraryBaseCollection, null=True)
    budget = IntegerField()
    homepage = TextField(null=True)
    imdb_id = CharField(max_length=9, null=True)
    original_language = TextField()
    original_title = TextField()
    overview = TextField(null=True)
    popularity = IntegerField()
    poster_path = TextField(null=True)
    release_date = DateField(formats=["%y-%m-%d"])
    revenue = IntegerField()
    runtime = IntegerField(null=True)
    status = CharField(max_length=15)
    tagline = TextField(null=True)
    title = TextField()
    video = BooleanField()
    vote_average = DoubleField()
    vote_count = IntegerField()


class LibraryBaseMovieGenres(TableBase):
    """Library Base Movie Genres"""

    movie = ForeignKeyField(LibraryBaseMovie, backref="genres")
    genre = ForeignKeyField(ScraperGenreMovies)


class LibraryBaseMovieProductionCompanies(TableBase):
    """Library Base Movie Production Companies"""

    movie = ForeignKeyField(LibraryBaseMovie, backref="production_companies")
    company = ForeignKeyField(LibraryBaseCompanies, backref="movies")


class LibraryBaseMovieProductionCountries(TableBase):
    """Library Base Movie Production Countries"""

    movie = ForeignKeyField(LibraryBaseMovie, backref="production_countries")
    country = ForeignKeyField(ScraperCountries, ScraperCountries.iso_3166_1, "movies")


class LibraryBaseMovieSpokenLanguages(TableBase):
    """Library Base Movie Spoken Languages"""

    movie = ForeignKeyField(LibraryBaseMovie, backref="spoken_languages")
    iso_639_1 = CharField(max_length=2)
