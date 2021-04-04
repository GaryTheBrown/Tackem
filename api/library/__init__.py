"""LIBRARY ROOT API"""
import cherrypy

from api.base import APIBase
from api.e404 import API404


@cherrypy.expose
class APILibrary(APIBase):
    """ROOT API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""
        if len(vpath) == 0:
            return self

        if len(vpath) == 1:
            section = vpath.pop(0)
            if section == "scan":
                return self
            if section == "check":
                return self
            if section == "list":
                return self

        if section == "games":
            return self
        if section == "movies":
            return self
        if section == "tvshows":
            return self
        if section == "music":
            return self

        return API404()

    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        """GET Function"""
        action = kwargs.get("action", None)

        return self._return_data("admin", action, True)
