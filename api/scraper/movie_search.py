"""Get Tv Show API"""
import cherrypy

from api.base import APIBase
from libs.scraper import Scraper


@cherrypy.expose
class APIScraperMovieSearch(APIBase):
    """Base Template For the API"""

    def GET(self, **kwargs) -> str:
        """POST Function"""

        if "name" not in kwargs:
            return self._return_data(
                "Scraper",
                "Movie Search",
                False,
                error="Missing Name",
                errorNumber=0,
            )

        data = Scraper.search_for_movie(
            kwargs["name"], kwargs.get("page", 1), kwargs.get("year", None)
        )
        return self._return_data(
            "Scraper", "Movie Search", True, data=data, images=Scraper.image_config
        )
