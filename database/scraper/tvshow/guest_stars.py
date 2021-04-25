"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.tvshow.cast import ScraperTVShowCast
from database.scraper.tvshow.episode import ScraperTVShowEpisode


class ScraperTVShowGuestStars(ScraperTVShowCast):
    """Library Base TV Show Cast"""

    episode = ForeignKeyField(ScraperTVShowEpisode, backref="guest_stars")
