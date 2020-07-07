'''SYSTEM API'''
import cherrypy
from system.full import TackemSystemFull
from system.plugin import TackemSystemPlugin
from api.base import APIBase

@cherrypy.expose
class APISystem(APIBase):
    '''SYSTEM API'''

# plugin manager api here
    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''
        plugin_type = vpath.pop(0)
        plugin_name = vpath.pop(0)
        plugin_instance = None
        plugin = TackemSystemFull().plugin(plugin_type, plugin_name)
        single_instance = plugin.SETTINGS["single_instance"]
        if not single_instance:
            plugin_instance = vpath.pop(0)

        # plugin_system = TackemSystemPlugin(plugin_type, plugin_name, plugin_instance)

        return self
