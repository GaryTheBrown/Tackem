from libs.authenticator import Authentication
import cherrypy
from libs.html_template import HTMLTEMPLATE
from libs.ripper import Ripper

class RipperDrive(HTMLTEMPLATE):
    '''ROOT OF PLUGINS WEBUI HERE'''

    def _return(self):
        '''return on fail'''
        raise cherrypy.HTTPRedirect(self._baseurl + "ripping/")

    @cherrypy.expose
    def index(self):
        '''index page return to ripper main page'''
        self._return()

    @cherrypy.expose
    def single(self, index=None):
        '''get single Drive'''
        Authentication.check_auth()
        if index is None:
            self._return()
        try:
            index_int = int(index)
        except ValueError:
            self._return()
        drives = Ripper.get_drives
        if index_int > len(drives):
            self._return()
        drive = drives[index_int]
        return drive.html_data()
