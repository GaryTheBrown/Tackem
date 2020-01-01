'''ROOT API'''
import json
import cherrypy
from api.base import APIBase
from api.config import APIConfig
from api.plugin import APIPlugin
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
        if section == "reboot":
            cherrypy.request.params['action'] = "reboot"
        elif section == "shutdown":
            cherrypy.request.params['action'] = "shutdown"
        elif section == "config":
            return APIConfig()
        elif section == "plugins":
            return APIPlugin()
        elif section == "system":
            return APISystem()
        # elif section == "":
        # elif section == "":
        # elif section == "":
        # elif section == "":
        # elif section == "":
        return self


    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        user = kwargs.get("user", self.GUEST)
        action = kwargs.get("action", None)
        if user == self.GUEST:
            raise cherrypy.HTTPError(status=401)  #Unauthorized
        if user == self.MASTER:
            if action == "shutdown":
                print("SHOULD SHUTDOWN")
                RootEvent.set_event("shutdown")
            elif action == "reboot":
                RootEvent.set_event("reboot")

        return json.dumps({
            "message" : "SUCCESS IN API KEY",
            "user" : user,
            "action": action
        })


    def _check_api_key(self, key: str) -> int:
        '''checks the api key against the master and user keys and returns the level'''
        masterapi = CONFIG["api"]["masterapi"]["key"].value
        userapi = CONFIG["api"]["userapi"]["key"].value
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
