"""Base Template For the API"""
import cherrypy

from api.base import APIBase
from libs.authentication import Authentication
from libs.ripper import Ripper


@cherrypy.expose
class APIRipperDrivesData(APIBase):
    """Base Template For the API"""

    def GET(self, id: int, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""
        user = kwargs.get("user", Authentication.GUEST)
        if user == Authentication.GUEST:
            raise cherrypy.HTTPError(status=403)
        try:
            index = int(id)
        except ValueError:
            raise cherrypy.HTTPError(status=400)

        drives = Ripper.drives
        if index > len(drives):
            raise cherrypy.HTTPError(status=404)
        drive_dict = drives[index].api_data()
        return self._return_data(
            user, "Ripper", f"Drive Info {index}", True, id=index, **drive_dict
        )
