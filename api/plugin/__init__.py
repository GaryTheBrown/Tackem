'''PLUGIN API'''
import json
import cherrypy
from system.full import TackemSystemFull
from .base import APIBase
from .download import APIPluginDownload

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

        return self
