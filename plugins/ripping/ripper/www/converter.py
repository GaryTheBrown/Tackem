'''Converter pages'''
import json
import cherrypy
from libs.html_template import HTMLTEMPLATE
from . import html_parts

class Converter(HTMLTEMPLATE):
    '''CONVERTER WEBUI'''
    @cherrypy.expose
    def index(self):
        '''index of plugin'''
        root_html = html_parts.get_page("converter/index", self._system)
        data = self._system.get_converter().get_quick_data()
        converter_html = html_parts.converter_items(data)
        root_html = root_html.replace("%%CONVERTERS%%", converter_html)
        return self._template(root_html)

    @cherrypy.expose
    def single(self, index=None):
        '''get single converter item'''
        if index is None:
            return self._redirect(self._baseurl + "ripping/ripper/converter/")
        try:
            index_int = int(index)
        except ValueError:
            return self._redirect(self._baseurl + "ripping/ripper/converter/")
        data = self._system.get_converter().get_quick_data_by_id(index_int)
        if data is False:
            return self._redirect(self._baseurl + "ripping/ripper/converter/")
        return html_parts.converter_item(data)

    @cherrypy.expose
    def getids(self):
        '''index of Drives'''
        return json.dumps(self._system.get_converter().get_data_ids())
