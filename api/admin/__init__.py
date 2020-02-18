'''ROOT API'''
import json
import cherrypy
from api.base import APIBase
from api.admin.config import APIAdminConfig
from api.admin.plugin import APIPlugin
from libs.root_event import RootEvent

@cherrypy.expose
class APIAdmin(APIBase):
    '''ROOT API'''


    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''
        if len(vpath) == 0:
            return self

        section = vpath.pop(0)
        if section == "reboot":
            cherrypy.request.params['action'] = "reboot"
        elif section == "shutdown":
            cherrypy.request.params['action'] = "shutdown"
        elif section == "config":
            return APIAdminConfig()
        elif section == "plugin":
            return APIPlugin()
        return self


    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        user = kwargs.get("user", self.GUEST)
        action = kwargs.get("action", None)

        if user != self.MASTER:
            raise cherrypy.HTTPError(status=401)  #Unauthorized

        if action == "shutdown":
            print("SHOULD SHUTDOWN")
            RootEvent.set_event("shutdown")
        elif action == "reboot":
            RootEvent.set_event("reboot")
        else:
            raise cherrypy.HTTPError(status=404)  #Not Found

        return self._return_data(user, "admin", action, True)
