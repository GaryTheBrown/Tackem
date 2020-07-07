'''Base Template For the API'''
from typing import Optional
import json
import cherrypy

class APIBase():
    '''Base Template For the API'''

    GUEST = 0
    MASTER = 1
    USER = 2
    PLUGIN = 3

    def GET(self, **kwargs) -> None:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        raise cherrypy.HTTPError(status=404)

    def POST(self, **kwargs) -> None:  # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        raise cherrypy.HTTPError(status=404)

    def PUT(self, **kwargs) -> None:  # pylint: disable=invalid-name,no-self-use
        '''PUT Function'''
        raise cherrypy.HTTPError(status=404)

    def DELETE(self, **kwargs) -> None:  # pylint: disable=invalid-name,no-self-use
        '''DELETE Function'''
        raise cherrypy.HTTPError(status=404)

    def _get_request_body(self) -> str:
        '''gets the requests body and returns dict'''
        content_length = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(content_length))
        return json.loads(rawbody)

    def _check_user(self, user: int, is_admin: bool = False) -> None:
        '''checks that the user is allowed'''
        if user == self.GUEST or (is_admin and user == self.USER):
            raise cherrypy.HTTPError(status=401)  # Unauthorized

    def _return_data(self, user: int, system: str, action: str, success: bool, **kwargs) -> str:
        '''creates the json for returning requiring some data but allowing more'''
        base = {
            "user": user,
            "system": system,
            "action": action,
            "success": success
        }

        for key, value in kwargs.items():
            base[key] = value

        return base

    def _actions_return(
            self,
            enable: Optional[list] = None,
            disable: Optional[list] = None,
            show: Optional[list] = None,
            hide: Optional[list] = None,
            rename: Optional[dict] = None
    ) -> dict:
        '''Creates the plugin data to return'''
        return {
            'enable': enable,
            'disable': disable,
            'show': show,
            'hide': hide,
            'rename': rename
        }
