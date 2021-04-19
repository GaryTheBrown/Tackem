"""Base Template For the API"""
import cherrypy

from api.base import APIBase
from libs.scraper import Scraper


@cherrypy.expose
class APIScraperMovieTMDBID(APIBase):
    """Base Template For the API"""

    def GET(self, **kwargs) -> str:
        """GET Function"""

        if "tmdbid" not in kwargs:
            return self._return_data(
                "Scraper",
                "Grab By TMDBID",
                False,
                error="Missing TMDBID",
                errorNumber=0,
            )

        data = Scraper.get_movie_details(kwargs["tmdbid"])

        return self._return_data(
            "Scraper", "Grab By TMDBID", True, data=data, images=Scraper.image_config
        )
