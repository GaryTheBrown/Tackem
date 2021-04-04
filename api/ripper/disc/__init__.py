"""RIPPER DRIVES API"""
import cherrypy

from api.base import APIBase
from api.e404 import API404
from api.ripper.disc.blank import APIRipperDiscBlank
from api.ripper.disc.disc_type_select import APIRipperDiscDiscTypeSelect


@cherrypy.expose
class APIRipperDisc(APIBase):
    """Ripper Drives API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""

        if len(vpath) == 0:
            return self
        section = vpath.pop(0)
        if section == "blank":
            return APIRipperDiscBlank()
        if section == "disctypeselect":
            return APIRipperDiscDiscTypeSelect()
        return API404()
