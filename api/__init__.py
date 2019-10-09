'''ROOT API'''
import json
import cherrypy
from system.full import TackemSystemFull
from libs.root_event import RootEvent
from .base import APIBase
from .config import APIConfig
from .plugin import APIPlugin
from .system import APISystem


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


    def GET(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
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


    def _check_api_key(self, key):
        '''checks the api key against the master and user keys and returns the level'''
        _, masterapi = TackemSystemFull().get_config(["masterapi", "key"], None)
        _, userapi = TackemSystemFull().get_config(["userapi", "key"], None)
        if key is None or not isinstance(key, str):
            return self.GUEST
        if key == "aaa": ## masterapi:
            return self.MASTER
        if key == "bbb": ## userapi:
            return self.USER
        if key == "ccc":
            return self.PLUGIN
        return self.GUEST


    def _check_session_id(self):
        '''checks the session Id is in the list'''
        if not TackemSystemFull().auth.check_logged_in():
            return self.GUEST
        if TackemSystemFull().auth.is_admin():
            return self.MASTER
        return self.USER


    def _check_user(self, user, is_admin=False):
        '''checks that the user is allowed'''
        if user == self.GUEST or (is_admin and user == self.USER):
            raise cherrypy.HTTPError(status=401)  #Unauthorized
