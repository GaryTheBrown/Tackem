"""Base Template For the API"""
import cherrypy

from api.base import APIBase
from libs.scraper import Scraper


@cherrypy.expose
class APIScraperSearchTV(APIBase):
    """Base Template For the API"""

    def GET(self, **kwargs) -> str:
        """POST Function"""

        if "name" not in kwargs:
            return self._return_data(
                "Scraper",
                "TV Show Search",
                False,
                error="Missing Name",
                errorNumber=0,
            )

        data = Scraper.search_for_tvshow(kwargs["name"], kwargs.get("page", 1))
        return self._return_data(
            "Scraper", "TV Show Search", True, data=data, images=Scraper.image_config
        )
