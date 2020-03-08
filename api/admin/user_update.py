'''User Update API'''
import cherrypy
from api.base import APIBase
from libs.authenticator import AUTHENTICATION


@cherrypy.expose
class APIAdminUserUpdate(APIBase):
    '''User Update API'''


    def POST(self, **kwargs) -> str:
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        body = self._get_request_body()

        if not "userId" in body:
            return self._return_data(
                user,
                "User",
                "Add User",
                False,
                error="Missing User ID",
                errorNumber=0
            )
        if not "username" in body:
            return self._return_data(
                user,
                "User",
                "Add User",
                False,
                error="Missing User Name",
                errorNumber=1
            )
        if not "password" in body:
            return self._return_data(
                user,
                "User",
                "Add User",
                False,
                error="Missing User Password",
                errorNumber=2
            )
        if not "isadmin" in body:
            return self._return_data(
                user,
                "User",
                "Add User",
                False,
                error="Missing is admin Setting",
                errorNumber=3
            )

        AUTHENTICATION.update_user(
            body['userid'],
            body['username'],
            body['password'],
            body['isadmin']
        )
        return self._return_data(
            user,
            "User",
            "Update User",
            True
        )
