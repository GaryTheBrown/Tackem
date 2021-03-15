"""User Update API"""
import cherrypy

from api.base import APIBase
from libs.authenticator import Authentication


@cherrypy.expose
class APIAdminUserUpdate(APIBase):
    """User Update API"""

    def POST(self, **kwargs) -> str:
        """POST Function"""
        user = kwargs.get("user", self.GUEST)

        if "userid" not in kwargs:
            return self._return_data(
                user, "User", "Add User", False, error="Missing User ID", errorNumber=0
            )
        if "username" not in kwargs:
            return self._return_data(
                user,
                "User",
                "Add User",
                False,
                error="Missing User Name",
                errorNumber=1,
            )
        if "password" not in kwargs:
            return self._return_data(
                user,
                "User",
                "Add User",
                False,
                error="Missing User Password",
                errorNumber=2,
            )
        if "isadmin" not in kwargs:
            return self._return_data(
                user,
                "User",
                "Add User",
                False,
                error="Missing is admin Setting",
                errorNumber=3,
            )
        Authentication.update_user(
            kwargs["userid"],
            kwargs["username"],
            kwargs["password"],
            bool(kwargs["isadmin"]),
        )
        return self._return_data(user, "User", "Update User", True)
