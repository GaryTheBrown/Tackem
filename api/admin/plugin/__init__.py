'''PLUGIN API'''
import json
import cherrypy
from api.base import APIBase

@cherrypy.expose
class APIAdminPlugin(APIBase):
    '''PLUGIN API'''

    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''
        action = vpath.pop(0).lower()

        return self
