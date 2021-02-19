'''ROOT API'''
from api.scraper import APIScraper
import cherrypy
from api.base import APIBase
from api.admin import APIAdmin
from api.library import APILibrary
from data.config import CONFIG
from libs.authenticator import Authentication

@cherrypy.expose
class API(APIBase):
    '''ROOT API'''

    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''
        user = None
        if len(vpath) == 0:
            return self

        api_key = vpath.pop(0)
        user = self._check_api_key(api_key)
        section = ""
        if user == self.GUEST:
            user = self._check_session_id()
        cherrypy.request.params['user'] = user
        if len(api_key) != 40:
            section = api_key
        else:
            if len(vpath) == 0:
                return self
            section = vpath.pop(0)

        if section == "admin":
            return APIAdmin()
        if section == "library":
            return APILibrary()
        if section == "scraper":
            return APIScraper()
        return self

    def _check_api_key(self, key: str) -> int:
        '''checks the api key against the master and user keys and returns the level'''
        if key is None or not isinstance(key, str):
            return self.GUEST
        if key == CONFIG["api"]["masterkey"].value:
            return self.MASTER
        if key == CONFIG["api"]["userkey"].value:
            return self.USER
        return self.GUEST

    def _check_session_id(self) -> int:
        '''checks the session Id is in the list'''
        if not Authentication.check_logged_in():
            return self.GUEST
        if Authentication.is_admin():
            return self.MASTER
        return self.USER
