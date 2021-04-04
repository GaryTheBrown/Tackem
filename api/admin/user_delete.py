"""User Delete API"""
import cherrypy

from api.base import APIBase
from libs.authentication import Authentication


@cherrypy.expose
class APIAdminUserDelete(APIBase):
    """User Delete API"""

    def POST(self, **kwargs) -> str:
        """POST Function"""
        self._check_user(True)
        if "userid" not in kwargs:
            return self._return_data(
                "User",
                "Update User",
                False,
                error="Missing User Id",
                errorNumber=0,
            )
        Authentication.delete_user(kwargs["userid"])
        return self._return_data("User", "Update User", True)
