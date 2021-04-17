"""ROOT API"""
import cherrypy

from api.admin import APIAdmin
from api.base import APIBase
from api.e404 import API404
from api.library import APILibrary
from api.ripper import APIRipper
from api.scraper import APIScraper
from config import CONFIG
from libs.auth import Auth


@cherrypy.expose
class API(APIBase):
    """ROOT API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""
        user = 0
        if len(vpath) == 0:
            return self

        section = ""
        api_key = vpath.pop(0)
        if len(api_key) == 40:
            user = self._check_api_key(api_key)
            if len(vpath) == 0:
                return self
            section = vpath.pop(0).lower()
        else:
            user = Auth.check_logged_in()
            section = api_key.lower()

        cherrypy.request.params["user"] = user

        if section == "admin":
            return APIAdmin()
        if section == "library":
            return APILibrary()
        if section == "ripper":
            return APIRipper()
        if section == "scraper":
            return APIScraper()
        return API404()

    def _check_api_key(self, key: str) -> int:
        """checks the api key against the master and user keys and returns the level"""
        if key is None or not isinstance(key, str):
            return Auth.GUEST
        if key == CONFIG["api"]["masterkey"].value:
            return Auth.ADMIN
        if key == CONFIG["api"]["userkey"].value:
            return Auth.USER
        return Auth.GUEST
