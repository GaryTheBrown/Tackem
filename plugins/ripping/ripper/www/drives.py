'''drives pages'''
import cherrypy
from libs.html_template import HTMLTEMPLATE
from . import html_parts

class Drives(HTMLTEMPLATE):
    '''DRIVES WEBUI'''
    @cherrypy.expose
    def index(self):
        '''index of Drives'''
        self._auth.check_auth()
        index_html = html_parts.get_page("drives/index", self._system)
        index_html = index_html.replace("%%DRIVES%%",
                                        html_parts.drives(self._system.get_drives(),
                                                          self._config['drives']))
        return self._template(index_html)

    @cherrypy.expose
    def single(self, index=None):
        '''get single Drive'''
        self._auth.check_auth()
        if index is None:
            raise cherrypy.HTTPRedirect(self._baseurl + "ripping/ripper/drives/")
        try:
            index_int = int(index)
        except ValueError:
            raise cherrypy.HTTPRedirect(self._baseurl + "ripping/ripper/drives/")
        drives = self._system.get_drives()
        if index_int > len(drives):
            raise cherrypy.HTTPRedirect(self._baseurl + "ripping/ripper/drives/")
        drive = self._system.get_drives()[index_int]
        return drive.html_data()
