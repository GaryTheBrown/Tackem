"""Get Tv Show API"""
import cherrypy

from api.base import APIBase

# from libs.scraper import Scraper


@cherrypy.expose
class APIScraperMovieSearch(APIBase):
    """Get Tv Show API"""

    def GET(self, **kwargs) -> str:
        """POST Function"""

        # Scraper.
        return self._return_data(
            "Scraper",
            "",
            True,
        )
