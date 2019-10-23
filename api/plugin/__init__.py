'''PLUGIN API'''
import json
import cherrypy
from system.full import TackemSystemFull
from .base import APIBase
from .download import APIPluginDownload
from .delete import APIPluginDelete
from .reload import APIPluginReload
from .start import APIPluginStart
from .stop import APIPluginStop
from .clear_config import APIPluginClearConfig
from .clear_database import APIPluginClearDatabase

@cherrypy.expose
class APIPlugin(APIBase):
    '''PLUGIN API'''

#plugin control api here
#this file will deal with starting and stopping plugins.
#maybe include install and remove commands in here
    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''
        action = vpath.pop(0).lower()
        cherrypy.request.params['action'] = action


        plugin_type = vpath.pop(0)
        plugin_name = vpath.pop(0)

        cherrypy.request.params['plugin_type'] = plugin_type
        cherrypy.request.params['plugin_name'] = plugin_name

        plugin_instance = None
        plugin = TackemSystemFull().plugin(plugin_type, plugin_name)
        single_instance = plugin.SETTINGS["single_instance"]
        if not single_instance:
            plugin_instance = vpath.pop(0)
            cherrypy.request.params['plugin_instance'] = plugin_instance

        if action == "download":
            return APIPluginDownload()

        if action == "delete":
            return APIPluginDelete()

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
