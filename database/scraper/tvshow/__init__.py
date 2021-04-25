"""Library Base Table"""
from peewee import BooleanField
from peewee import CharField
from peewee import DateField
from peewee import DoubleField
from peewee import IntegerField
from peewee import TextField

from database.scraper.base import ScraperBaseTable


class ScraperTVShow(ScraperBaseTable):
    """Library Base TV Show"""

    backdrop_path = TextField(null=True)
    first_air_date = DateField(formats=["%y-%m-%d"])
    homepage = TextField()
    in_production = BooleanField()
    last_air_date = DateField(formats=["%y-%m-%d"])
    # last_episode_to_air
    name = TextField()
    next_episode_to_air = TextField(null=True)
    number_of_episodes = IntegerField()
    number_of_seasons = IntegerField()
    original_language = CharField(max_length=2)
    original_name = TextField()
    overview = TextField()
    popularity = DoubleField()
    poster_path = TextField(null=True)
    status = TextField()
    tagline = TextField()
    type = TextField()
    vote_average = DoubleField()
    vote_count = IntegerField()
