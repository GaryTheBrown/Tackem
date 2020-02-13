'''ROOT API'''
import json
import cherrypy
from api.base import APIBase
from api.admin import APIAdmin
from api.system import APISystem
from config_data import CONFIG
from libs.root_event import RootEvent
from libs.authenticator import AUTHENTICATION


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
        if user == self.GUEST:
            user = self._check_session_id()
        cherrypy.request.params['user'] = user
        if len(vpath) == 0:
            return self

        section = vpath.pop(0)
        if section == "admin":
            return APIAdmin()
        if section == "system":
            return APISystem()
        # if section == "":
        # if section == "":
        # if section == "":
        # if section == "":
        # if section == "":
        return self


    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        user = kwargs.get("user", self.GUEST)
        return json.dumps({
            "message" : "SUCCESS IN API KEY",
            "user" : user,
        })


    def _check_api_key(self, key: str) -> int:
        '''checks the api key against the master and user keys and returns the level'''
        masterapi = CONFIG["api"]["masterkey"].value
        userapi = CONFIG["api"]["userkey"].value
        if key is None or not isinstance(key, str):
            return self.GUEST
        if key == masterapi:
            return self.MASTER
        if key == userapi:
            return self.USER
        # if key == "ccc":
        #     return self.PLUGIN
        return self.GUEST


    def _check_session_id(self) -> int:
        '''checks the session Id is in the list'''
        if not AUTHENTICATION.check_logged_in():
            return self.GUEST
        if AUTHENTICATION.is_admin():
            return self.MASTER
        return self.USER
