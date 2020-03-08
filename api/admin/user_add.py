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
        body = self._get_request_body()
        if not "username" in body:
            return self._return_data(
                user,
                "User",
                "Add User",
                False,
                error="Missing User Name",
                errorNumber=0
            )
        if not "password" in body:
            return self._return_data(
                user,
                "User",
                "Add User",
                False,
                error="Missing User Password",
                errorNumber=1
            )
        if not "isadmin" in body:
            return self._return_data(
                user,
                "User",
                "Add User",
                False,
                error="Missing is admin Setting",
                errorNumber=2
            )

        AUTHENTICATION.add_user(body['username'], body['password'], body['isadmin'])
        return self._return_data(
            user,
            "User",
            "Add User",
            True
        )
