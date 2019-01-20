'''drives pages'''
import cherrypy
from libs.html_template import HTMLTEMPLATE
from . import html_parts

class Drives(HTMLTEMPLATE):
    '''ROOT OF PLUGINS WEBUI HERE'''
    @cherrypy.expose
    def index(self):
        '''index of Drives'''
        index_html = html_parts.get_page("drives/index", self._system)
        index_html = index_html.replace("%%DRIVES%%",
                                        html_parts.drives(self._system.get_drives(),
                                                          self._config['drives']))
        return self._template(index_html)

    @cherrypy.expose
    def single(self, index=None):
        '''get single Drive'''
        if index is None:
            return "FAILED No Index"
        try:
            index_int = int(index)
        except ValueError:
            return "Failed Not an Index"
        drives = self._system.get_drives()
        if index_int > len(drives):
            return "Failed Index Out Of Range"
        drive = self._system.get_drives()[index_int]
        return drive.html_data()
