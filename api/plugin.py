'''PLUGIN API'''
import json
import cherrypy
from system.full import TackemSystemFull
from .base import APIBase


@cherrypy.expose
class APIPlugin(APIBase):
    '''PLUGIN API'''

#plugin control api here
#this file will deal with starting and stopping plugins.
#maybe include install and remove commands in here
    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''
        action = vpath.pop(0)
        plugin_type = vpath.pop(0)
        plugin_name = vpath.pop(0)


        plugin_instance = None
        plugin = TackemSystemFull().plugin(plugin_type, plugin_name)
        single_instance = plugin.SETTINGS["single_instance"]
        if not single_instance:
            plugin_instance = vpath.pop(0)



        return self
