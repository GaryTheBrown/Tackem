'''Root pages'''
import cherrypy
from libs.html_template import HTMLTEMPLATE
from . import html_parts

class Root(HTMLTEMPLATE):
    '''ROOT OF PLUGINS WEBUI HERE'''
    @cherrypy.expose
    def index(self):
        '''index of plugin'''
        root_html = html_parts.get_page("root", False)
        root_html = root_html.replace("%%DRIVES%%", html_parts.drives(self._system.get_drives(),
                                                                      self._config['drives'], True))
        return self._template(root_html)
