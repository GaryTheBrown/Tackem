"""RIPPER API"""
import cherrypy

from api.base import APIBase
from api.e404 import API404
from api.ripper.data import APIRipperData
from api.ripper.disc import APIRipperDisc
from api.ripper.drives import APIRipperDrives
from api.ripper.iso import APIRipperIsos
from api.ripper.video_converter import APIRipperVideoConverter
from config import CONFIG


@cherrypy.expose
class APIRipper(APIBase):
    """Ripper API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""

        if not CONFIG["ripper"]["enabled"].value or len(vpath) == 0:
            return self

        section = vpath.pop(0).lower()

        if section == "data":
            return APIRipperData()
        if section == "disc":
            return APIRipperDisc()
        if section == "drives":
            return APIRipperDrives()
        if section == "iso":
            return APIRipperIsos()
        if section == "videoconverter":
            return APIRipperVideoConverter()
        return API404()
