'''ADMIN ROOT API'''
import cherrypy
from api.base import APIBase
from api.admin.config import APIAdminConfig
from api.admin.plugin import APIAdminPlugin
from api.admin.add_multi import APIAdminAddMulti
from api.admin.delete_multi import APIAdminDeleteMulti
from api.admin.user_add import APIAdminUserAdd
from api.admin.user_delete import APIAdminUserDelete
from api.admin.user_update import APIAdminUserUpdate
from libs.root_event import RootEvent

@cherrypy.expose
class APIAdmin(APIBase):
    '''ROOT API'''

    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''
        if len(vpath) == 0:
            return self

        if cherrypy.request.params['user'] != self.MASTER:
            raise cherrypy.HTTPError(status=401)  # Unauthorized

        section = vpath.pop(0)
        if section == "reboot":
            cherrypy.request.params['action'] = "reboot"
        elif section == "shutdown":
            cherrypy.request.params['action'] = "shutdown"
        elif section == "config":
            return APIAdminConfig()
        elif section == "addMulti":
            return APIAdminAddMulti()
        elif section == "deleteMulti":
            return APIAdminDeleteMulti()
        elif section == "plugin":
            return APIAdminPlugin()
        elif section == "userAdd":
            return APIAdminUserAdd()
        elif section == "userDelete":
            return APIAdminUserDelete()
        elif section == "userUpdate":
            return APIAdminUserUpdate()
        return self

    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        user = kwargs.get("user", self.GUEST)
        action = kwargs.get("action", None)

        if action == "shutdown":
            print("SHOULD SHUTDOWN")
            RootEvent.set_event("shutdown")
        elif action == "reboot":
            RootEvent.set_event("reboot")
        else:
            raise cherrypy.HTTPError(status=404)  # Not Found

        return self._return_data(user, "admin", action, True)
