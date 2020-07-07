'''PLUGIN API'''
import json
import cherrypy
from system.full import TackemSystemFull
from api.base import APIBase
from api.admin.plugin.download import APIPluginDownload
from api.admin.plugin.update import APIPluginUpdate
from api.admin.plugin.load import APIPluginLoad
from api.admin.plugin.unload import APIPluginUnload

@cherrypy.expose
class APIAdminPlugin(APIBase):
    '''PLUGIN API'''

    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''
        action = vpath.pop(0).lower()

        if action == "download":
            return APIPluginDownload()
        if action == "update":
            return APIPluginUpdate()
        if action == "load":
            return APIPluginLoad()
        if action == "unload":
            return APIPluginUnload()
        return self
