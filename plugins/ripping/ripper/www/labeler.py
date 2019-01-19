'''Labeler pages'''
import json
import cherrypy
from libs.html_template import HTMLTEMPLATE
from . import html_parts

class Labeler(HTMLTEMPLATE):
    '''LABELER OF PLUGINS WEBUI HERE'''
    @cherrypy.expose
    def index(self):
        '''index of plugin'''
        root_html = html_parts.get_page("labeler/index")
        data = self._system.get_labeler().get_data("WWW" + cherrypy.request.remote.ip)
        root_html = root_html.replace("%%DATA%%", json.dumps(data))
        return self._template(root_html)
