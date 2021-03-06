'''User Add API'''
import cherrypy
from api.base import APIBase
from libs.authenticator import AUTHENTICATION

@cherrypy.expose
class APIAdminUserAdd(APIBase):
    '''User Add API'''

    def POST(self, **kwargs) -> str:
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        if "username" not in kwargs:
            return self._return_data(
                user,
                "User",
                "Add User",
                False,
                error="Missing User Name",
                errorNumber=0
            )
        if "password" not in kwargs:
            return self._return_data(
                user,
                "User",
                "Add User",
                False,
                error="Missing User Password",
                errorNumber=1
            )
        if "isadmin" not in kwargs:
            return self._return_data(
                user,
                "User",
                "Add User",
                False,
                error="Missing is admin Setting",
                errorNumber=2
            )
        AUTHENTICATION.add_user(
            kwargs['username'], kwargs['password'], bool(kwargs['isadmin']))
        return self._return_data(
            user,
            "User",
            "Add User",
            True
        )
