'''Root pages'''
import os
import cherrypy
from libs.html_template import HTMLTEMPLATE

class Root(HTMLTEMPLATE):
    '''ROOT OF PLUGINS WEBUI HERE'''
    @cherrypy.expose
    def index(self):
        '''index of plugin'''
        directory = os.path.dirname(__file__)
        index_page = str(open(directory + "/html/root.html", "r").read())
        return self._template(index_page)
