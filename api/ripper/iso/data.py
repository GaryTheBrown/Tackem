"""Base Template For the API"""
import cherrypy

from api.base import APIBase
from libs.authentication import Authentication
from libs.ripper import Ripper


@cherrypy.expose
class APIRipperISOData(APIBase):
    """Base Template For the API"""

    def GET(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""
        user = kwargs.get("user", Authentication.GUEST)
        if user == Authentication.GUEST:
            raise cherrypy.HTTPError(status=403)

        return self._return_data(
            user,
            "Ripper",
            "ISO Info",
            True,
            count=len(Ripper.isos),
            isos=[iso.api_data() for iso in Ripper.isos],
        )
