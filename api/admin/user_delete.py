"""User Delete API"""
import cherrypy

from api.base import APIBase
from libs.authentication import Authentication


@cherrypy.expose
class APIAdminUserDelete(APIBase):
    """User Delete API"""

    def POST(self, **kwargs) -> str:
        """POST Function"""
        if "userid" not in kwargs:
            return self._return_data(
                cherrypy.request.params["user"],
                "User",
                "Update User",
                False,
                error="Missing User Id",
                errorNumber=0,
            )
        Authentication.delete_user(kwargs["userid"])
        return self._return_data(cherrypy.request.params["user"], "User", "Update User", True)
