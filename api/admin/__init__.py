"""ADMIN ROOT API"""
import cherrypy

from api.admin.config import APIAdminConfig
from api.admin.user_add import APIAdminUserAdd
from api.admin.user_delete import APIAdminUserDelete
from api.admin.user_update import APIAdminUserUpdate
from api.base import APIBase
from api.e404 import API404
from libs.events import RootEvent


@cherrypy.expose
class APIAdmin(APIBase):
    """ROOT API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""
        if len(vpath) == 0:
            return self

        self._check_user(True)

        section = vpath.pop(0)
        if section == "reboot":
            cherrypy.request.params["action"] = "reboot"
        elif section == "shutdown":
            cherrypy.request.params["action"] = "shutdown"
        elif section == "config":
            return APIAdminConfig()
        elif section == "userAdd":
            return APIAdminUserAdd()
        elif section == "userDelete":
            return APIAdminUserDelete()
        elif section == "userUpdate":
            return APIAdminUserUpdate()
        return API404()

    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        """GET Function"""
        action = kwargs.get("action", None)

        if action == "shutdown":
            RootEvent.set_event("shutdown")
        elif action == "reboot":
            RootEvent.set_event("reboot")
        else:
            raise cherrypy.HTTPError(status=404)  # Not Found

        return self._return_data("admin", action, True)
