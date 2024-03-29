"""Base Template For the API"""
import cherrypy

from api.base import APIBase
from ripper import Ripper


@cherrypy.expose
class APIRipperISOData(APIBase):
    """Base Template For the API"""

    def GET(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""

        return self._return_data(
            "Ripper",
            "ISO Info",
            True,
            count=len(Ripper.isos),
            isos=[iso.api_data() for iso in Ripper.isos],
        )
