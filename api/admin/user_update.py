"""User Update API"""
import cherrypy

from api.base import APIBase
from libs.authentication import Authentication


@cherrypy.expose
class APIAdminUserUpdate(APIBase):
    """User Update API"""

    def POST(self, userid: str, **kwargs) -> str:
        """POST Function"""
        self._check_user(True)
        if "username" not in kwargs:
            return self._return_data(
                "User",
                "Add User",
                False,
                error="Missing User Name",
                errorNumber=0,
            )
        if "password" not in kwargs:
            return self._return_data(
                "User",
                "Add User",
                False,
                error="Missing User Password",
                errorNumber=1,
            )
        if "isadmin" not in kwargs:
            return self._return_data(
                "User",
                "Add User",
                False,
                error="Missing is admin Setting",
                errorNumber=2,
            )
        if Authentication.update_user(
            userid,
            kwargs["username"],
            kwargs["password"],
            kwargs["isadmin"] == "true",
        ):
            return self._return_data("User", "Update User", True)
        return self._return_data(
            "User",
            "Add User",
            False,
            error="Update Failed Due to Authentication",
            errorNumber=3,
        )
