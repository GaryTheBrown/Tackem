'''WEBUI FOR PLUGIN'''
import cherrypy
from libs.htmltemplate import HTMLTEMPLATE

LAYOUT = {}
CFG = {}

class Root(HTMLTEMPLATE):
    '''ROOT OF PLUGINS WEBUI HERE'''
    @cherrypy.expose
    def index(self):
        '''index of plugin'''
        index_page = self._name + " ROOT"
        return self._template(index_page)
