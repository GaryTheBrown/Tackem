'''ROOT API'''
import json
import cherrypy
from api.base import APIBase
from api.admin.config import APIConfig
from libs.root_event import RootEvent

@cherrypy.expose
class APIAdmin(APIBase):
    '''ROOT API'''


    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''
        user = cherrypy.request.params['user']
        if len(vpath) == 0:
            return self

        section = vpath.pop(0)
        if section == "reboot":
            cherrypy.request.params['action'] = "reboot"
        elif section == "shutdown":
            cherrypy.request.params['action'] = "shutdown"
        elif section == "config":
            return APIConfig()
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
