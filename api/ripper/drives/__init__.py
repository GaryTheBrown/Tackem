"""RIPPER DRIVES API"""
import cherrypy

from api.base import APIBase
from api.e404 import API404
from api.ripper.drives.data import APIRipperDrivesData
from data.config import CONFIG


@cherrypy.expose
class APIRipperDrives(APIBase):
    """Ripper Drives API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""

        if not CONFIG["ripper"]["drives"]["enabled"].value or len(vpath) == 0:
            return self

        section = vpath.pop(0).lower()

        if section == "data":
            return APIRipperDrivesData()
        return API404()
