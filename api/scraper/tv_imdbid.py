"""Get Tv Show API"""
import cherrypy

from api.base import APIBase
from libs.scraper import Scraper


@cherrypy.expose
class APIScraperTVIMDBID(APIBase):
    """Base Template For the API"""

    def GET(self, **kwargs) -> str:
        """GET Function"""

        if "imdbid" not in kwargs:
            return self._return_data(
                "Scraper",
                "Grab Movie By IMDBID",
                False,
                error="Missing IMDBID",
                errorNumber=0,
            )

        data = Scraper.tvshow_by_imdb_id(kwargs["imdbid"])

        return self._return_data(
            "Scraper", "Grab Movie By IMDBID", True, data=data, images=Scraper.image_config
        )
