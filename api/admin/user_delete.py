"""User Delete API"""
import cherrypy

from api.base import APIBase
from libs.authentication import Authentication


@cherrypy.expose
class APIAdminUserDelete(APIBase):
    """User Delete API"""

    def DELETE(self, userid: int, **kwargs) -> str:
        """DELETE Function"""
        self._check_user(True)
        Authentication.delete_user(userid)
        return self._return_data("User", "Update User", True)
