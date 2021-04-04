"""Base Template For the API"""
import cherrypy

from api.base import APIBase
from libs.ripper import Ripper


@cherrypy.expose
class APIRipperDrivesData(APIBase):
    """Base Template For the API"""

    def GET(self, id: int, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""
        try:
            index = int(id)
        except ValueError:
            raise cherrypy.HTTPError(status=400)

        drives = Ripper.drives
        if index > len(drives):
            raise cherrypy.HTTPError(status=404)
        drive_dict = drives[index].api_data()
        return self._return_data(
            cherrypy.request.params["user"],
            "Ripper",
            f"Drive Info {index}",
            True,
            id=index,
            **drive_dict,
        )
