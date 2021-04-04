"""User Update API"""
import cherrypy

from api.base import APIBase
from libs.authentication import Authentication


@cherrypy.expose
class APIAdminUserUpdate(APIBase):
    """User Update API"""

    def POST(self, **kwargs) -> str:
        """POST Function"""
        self._check_user()
        # TODO need to make this check if you are the user or you are admin
        if "userid" not in kwargs:
            return self._return_data(
                "User",
                "Add User",
                False,
                error="Missing User ID",
                errorNumber=0,
            )
        if "username" not in kwargs:
            return self._return_data(
                "User",
                "Add User",
                False,
                error="Missing User Name",
                errorNumber=1,
            )
        if "password" not in kwargs:
            return self._return_data(
                "User",
                "Add User",
                False,
                error="Missing User Password",
                errorNumber=2,
            )
        if "isadmin" not in kwargs:
            return self._return_data(
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
        return self._return_data("User", "Update User", True)
