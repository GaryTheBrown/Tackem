'''PLUGIN API'''
import json
import cherrypy
from system.full import TackemSystemFull
from api.base import APIBase
from api.plugin.download import APIPluginDownload
from api.plugin.delete import APIPluginDelete
from api.plugin.update import APIPluginUpdate
from api.plugin.reload import APIPluginReload
from api.plugin.start import APIPluginStart
from api.plugin.stop import APIPluginStop
from api.plugin.clear_config import APIPluginClearConfig
from api.plugin.clear_database import APIPluginClearDatabase

@cherrypy.expose
class APIPlugin(APIBase):
    '''PLUGIN API'''

    __SINGLE_ACTIONS = {
        "download": APIPluginDownload,
        "delete": APIPluginDelete,
        "update": APIPluginUpdate,
        "reload": APIPluginReload,
        "start": APIPluginStart,
        "stop": APIPluginStop,
        "clearconfig": APIPluginClearConfig,
        "cleardatabase": APIPluginClearDatabase
    }

    __ALL_ACTIONS = {

    }


    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''
        action = vpath.pop(0).lower()
        cherrypy.request.params['action'] = action

        #commands for no plugin names given
        if action in self.__ALL_ACTIONS:
            return self.__ALL_ACTIONS[action]()

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

        #commands for single plugin actions
        if action in self.__SINGLE_ACTIONS:
            return self.__SINGLE_ACTIONS[action]()

        return self
