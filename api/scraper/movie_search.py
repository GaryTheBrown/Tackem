"""Get Tv Show API"""
import cherrypy

from api.base import APIBase


@cherrypy.expose
class APIScraperMovieSearch(APIBase):
    """Get Tv Show API"""

    def POST(self, **kwargs) -> str:
        """POST Function"""

        return self._return_data(
            "Scraper",
            "",
            True,
        )
