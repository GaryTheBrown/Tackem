"""MUSIC LIBRARY ROOT API"""
import cherrypy

from api.base import APIBase


@cherrypy.expose
class APIMusicLibrary(APIBase):
    """ROOT API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""
        if len(vpath) == 0:
            return self

        if cherrypy.request.params["user"] != self.MASTER:
            raise cherrypy.HTTPError(status=401)  # Unauthorized

        if len(vpath) == 1:
            section = vpath.pop(0)
            if section == "scan":
                return self
            if section == "check":
                return self
            if section == "list":
                return self

        return self

    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        """GET Function"""
        user = kwargs.get("user", self.GUEST)
        action = kwargs.get("action", None)

        return self._return_data(user, "admin", action, True)
