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
        root_html = html_parts.get_page("labeler/index", self._system)
        data = self._system.get_labeler().get_data("WWW" + cherrypy.request.remote.ip)
        labeler_html = html_parts.labeleritems(data, self._baseurl, False)
        root_html = root_html.replace("%%LABELERS%%", labeler_html)
        return self._template(root_html)

    @cherrypy.expose
    def single(self, index=None, vertical=True):
        '''get single labeler item'''
        if index is None:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        try:
            index_int = int(index)
        except ValueError:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        data = self._system.get_labeler().get_data_by_id("WWW" + cherrypy.request.remote.ip,
                                                         index_int)
        if data is False:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        if isinstance(vertical, str):
            vertical = False
        return html_parts.labeleritem(data, self._baseurl, vertical)

    @cherrypy.expose
    def getids(self):
        '''index of Drives'''
        return json.dumps(self._system.get_labeler().get_ids("WWW" + cherrypy.request.remote.ip))

    @cherrypy.expose
    def edit(self, index):
        '''edit the data page'''
        if index is None:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        try:
            index_int = int(index)
        except ValueError:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        data = self._system.get_labeler().get_data_by_id("WWW" + cherrypy.request.remote.ip,
                                                         index_int)
        if data is False:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        return self._template(json.dumps(data))
