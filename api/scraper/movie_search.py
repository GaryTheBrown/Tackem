"""Get Tv Show API"""
import cherrypy

from api.base import APIBase
from libs.scraper import Scraper


@cherrypy.expose
class APIScraperMovieSearch(APIBase):
    """Get Tv Show API"""

    def GET(self, **kwargs) -> str:
        """POST Function"""

        data = Scraper.search_for_movie(
            kwargs["name"], kwargs.get("page", 1), kwargs.get("year", None)
        )
        return self._return_data("Scraper", "", True, data=data, images=Scraper.image_config)
