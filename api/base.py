"""Base Template For the API"""
import json
from typing import Optional

import cherrypy

from libs.auth import Auth


class APIBase:
    """Base Template For the API"""

    def GET(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""
        raise cherrypy.HTTPError(status=405)

    def POST(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """POST Function"""
        raise cherrypy.HTTPError(status=405)

    def PUT(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """PUT Function"""
        raise cherrypy.HTTPError(status=405)

    def DELETE(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """DELETE Function"""
        raise cherrypy.HTTPError(status=405)

    def _get_request_body(self) -> str:
        """gets the requests body and returns dict"""
        content_length = cherrypy.request.headers["Content-Length"]
        rawbody = cherrypy.request.body.read(int(content_length))
        return json.loads(rawbody)

    def _check_user(self, is_admin: bool = False):
        """checks that the user is allowed"""
        if is_admin and cherrypy.request.params["user"] < Auth.ADMIN:
            raise cherrypy.HTTPError(status=401)  # Unauthorized
        if cherrypy.request.params["user"] == Auth.GUEST:
            raise cherrypy.HTTPError(status=401)  # Unauthorized

    def _return_data(self, system: str, action: str, success: bool, **kwargs) -> str:
        """creates the json for returning requiring some data but allowing more"""
        base = {
            "user": cherrypy.request.params["user"],
            "class": self.__class__.__name__,
            "system": system,
            "action": action,
            "success": success,
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
        rename: Optional[dict] = None,
    ) -> dict:
        """Creates the plugin data to return"""
        return {
            "enable": enable,
            "disable": disable,
            "show": show,
            "hide": hide,
            "rename": rename,
        }
