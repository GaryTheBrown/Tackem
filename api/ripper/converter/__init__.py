"""RIPPER Converter API"""
import cherrypy

from api.base import APIBase
from api.ripper.converter.data import APIRipperConverterData
from data.config import CONFIG


@cherrypy.expose
class APIRipperConverter(APIBase):
    """Ripper Converter API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""

        if not CONFIG["ripper"]["converter"]["enabled"].value or len(vpath) == 0:
            return self

        section = vpath.pop(0)

        if section == "data":
            return APIRipperConverterData()
        return self
