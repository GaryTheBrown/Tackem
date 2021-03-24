"""All Data for the ripper Page"""
import cherrypy

from api.base import APIBase
from libs.ripper import Ripper


@cherrypy.expose
class APIRipperData(APIBase):
    """All Data for the ripper Page"""

    def GET(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""
        user = kwargs.get("user", self.GUEST)
        if user == self.GUEST:
            raise cherrypy.HTTPError(status=403)

        return self._return_data(
            user,
            "Ripper",
            "Full Info",
            True,
            drives=[drive.api_data() for drive in Ripper.drives],
            isos=[iso.api_data() for iso in Ripper.isos],
            converters=[con.api_data() for con in Ripper.video_converters],
        )
