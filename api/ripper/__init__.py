"""RIPPER API"""
import cherrypy

from api.base import APIBase
from api.ripper.drives import APIRipperDrives
from api.ripper.iso import APIRipperIsos
from data.config import CONFIG


@cherrypy.expose
class APIRipper(APIBase):
    """Ripper API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""

        if not CONFIG["ripper"]["enabled"].value or len(vpath) == 0:
            return self

        section = vpath.pop(0)

        if section == "drives":
            return APIRipperDrives()
        if section == "iso":
            return APIRipperIsos()
        return self
