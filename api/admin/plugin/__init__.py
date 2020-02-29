'''PLUGIN API'''
import json
import cherrypy
from system.full import TackemSystemFull
from api.base import APIBase
from api.admin.plugin.download import APIPluginDownload
from api.admin.plugin.delete import APIPluginDelete
from api.admin.plugin.update import APIPluginUpdate
from api.admin.plugin.reload import APIPluginReload
from api.admin.plugin.start import APIPluginStart
from api.admin.plugin.stop import APIPluginStop
from api.admin.plugin.clear_config import APIPluginClearConfig
from api.admin.plugin.clear_database import APIPluginClearDatabase

@cherrypy.expose
class APIAdminPlugin(APIBase):
    '''PLUGIN API'''

    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''
        action = vpath.pop(0).lower()

        if action == "download":
            return APIPluginDownload()
        if action == "delete":
            return APIPluginDelete()
        if action == "update":
            return APIPluginUpdate()
        if action == "reload":
            return APIPluginReload()
        if action == "start":
            return APIPluginStart()
        if action == "stop":
            return APIPluginStop()
        if action == "clearconfig":
            return APIPluginClearConfig()
        if action == "cleardatabase":
            return APIPluginClearDatabase()
        return self
