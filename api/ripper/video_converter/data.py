"""Base Template For the API"""
import cherrypy

from api.base import APIBase
from libs.authentication import Authentication
from libs.ripper import Ripper


@cherrypy.expose
class APIRipperVideoConverterData(APIBase):
    """Base Template For the API"""

    def GET(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""
        user = kwargs.get("user", Authentication.GUEST)
        if user == Authentication.GUEST:
            raise cherrypy.HTTPError(status=403)

        return self._return_data(
            user,
            "Ripper",
            "Video Converter Info",
            True,
            count=len(Ripper.video_converters),
            converters=[con.api_data() for con in Ripper.video_converters],
        )
