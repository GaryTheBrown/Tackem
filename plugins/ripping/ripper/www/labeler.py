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
        baseurl = self._global_config.get("webui", {}).get("baseurl", "/")
        root_html = html_parts.get_page("labeler/index", self._system)
        data = self._system.get_labeler().get_data("WWW" + cherrypy.request.remote.ip)
        labeler_html = html_parts.labeleritems(data, baseurl, False)
        root_html = root_html.replace("%%LABELERS%%", labeler_html)
        return self._template(root_html)

    @cherrypy.expose
    def single(self, index=None, vertical=True):
        '''get single labeler item'''
        if index is None:
            return "FAILED No Index"
        try:
            index_int = int(index)
        except ValueError:
            return "Failed Not an Index"
        data = self._system.get_labeler().get_data_by_id("WWW" + cherrypy.request.remote.ip,
                                                         index_int)
        if data is False:
            return "Failed Index Out Of Range"
        if isinstance(vertical, str):
            vertical = False
        baseurl = self._global_config.get("webui", {}).get("baseurl", "/")
        return html_parts.labeleritem(data, baseurl, vertical)

    @cherrypy.expose
    def getids(self):
        '''index of Drives'''
        return json.dumps(self._system.get_labeler().get_ids("WWW" + cherrypy.request.remote.ip))
