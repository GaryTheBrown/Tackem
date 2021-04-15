"""Get Tv Show API"""
import cherrypy

from api.base import APIBase
from libs.scraper import Scraper


@cherrypy.expose
class APIScraperTVTVDBID(APIBase):
    """Base Template For the API"""

    def GET(self, **kwargs) -> str:
        """GET Function"""

        if "tvdbid" not in kwargs:
            return self._return_data(
                "Scraper",
                "Grab TV Show By TVDBID",
                False,
                error="Missing TVDBID",
                errorNumber=0,
            )

        data = Scraper.tvshow_by_tvdb_id(kwargs["tvdbid"])

        return self._return_data(
            "Scraper", "Grab TV Show By TVDBID", True, data=data, images=Scraper.image_config
        )
