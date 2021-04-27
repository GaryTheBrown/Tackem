"""Library Base Table"""
from peewee import ForeignKeyField

from database.scraper.tvshow.cast import ScraperTVShowCast
from database.scraper.tvshow.episode import ScraperTVShowEpisode


class ScraperTVShowGuestStars(ScraperTVShowCast):
    """Library Base TV Show Cast"""

    episode = ForeignKeyField(ScraperTVShowEpisode, backref="guest_stars")

    @classmethod
    def from_data_dict(cls, data: dict, episode: ScraperTVShowEpisode) -> ScraperTVShowCast:
        """Generates the model from a dict"""
        guest_star = cls.get_or_create(id=data["id"])
        guest_star.tv_show = episode.tvshow
        guest_star.episode = episode
        guest_star.gender = data["gender"]
        guest_star.known_for_department = data["known_for_department"]
        guest_star.name = data["name"]
        guest_star.original_name = data["original_name"]
        guest_star.popularity = data["popularity"]
        guest_star.profile_path = data["profile_path"]
        guest_star.character = data["character"]
        guest_star.credit_id = data["credit_id"]
        guest_star.order = data["order"]
        guest_star.save()
        return guest_star
