'''Root pages'''
import cherrypy
from libs.html_template import HTMLTEMPLATE
from . import html_parts

class Root(HTMLTEMPLATE):
    '''ROOT OF PLUGINS WEBUI HERE'''
    @cherrypy.expose
    def index(self):
        '''index of plugin'''
        baseurl = self._global_config.get("webui", {}).get("baseurl", "/")
        root_html = html_parts.get_page("root/index", False)
        root_html = root_html.replace("%%DRIVES%%", html_parts.drives(self._system.get_drives(),
                                                                      self._config['drives'], True))
        data = self._system.get_labeler().get_data("WWW" + cherrypy.request.remote.ip)
        labeler_html = html_parts.labeler_items(data, baseurl, True)
        root_html = root_html.replace("%%LABELERS%%", labeler_html)
        return self._template(root_html)
