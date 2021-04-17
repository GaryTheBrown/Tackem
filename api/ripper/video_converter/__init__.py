"""RIPPER Converter API"""
import cherrypy

from api.base import APIBase
from api.e404 import API404
from api.ripper.video_converter.data import APIRipperVideoConverterData
from config import CONFIG


@cherrypy.expose
class APIRipperVideoConverter(APIBase):
    """Ripper Converter API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""

        if not CONFIG["ripper"]["converter"]["enabled"].value or len(vpath) == 0:
            return self

        section = vpath.pop(0).lower()

        if section == "data":
            return APIRipperVideoConverterData()
        return API404()
