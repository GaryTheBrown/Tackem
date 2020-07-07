'''User Delete API'''
import cherrypy
from api.base import APIBase
from libs.authenticator import AUTHENTICATION

@cherrypy.expose
class APIAdminUserDelete(APIBase):
    '''User Delete API'''

    def POST(self, **kwargs) -> str:
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        if "userid" not in kwargs:
            return self._return_data(
                user,
                "User",
                "Update User",
                False,
                error="Missing User Id",
                errorNumber=0
            )
        AUTHENTICATION.delete_user(kwargs['userid'])
        return self._return_data(
            user,
            "User",
            "Update User",
            True
        )
