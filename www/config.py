'''Script For the Config System'''
import cherrypy
# from libs import html_parts
from libs.authenticator import AUTHENTICATION
from libs.config.html.post_to_config import post_config_settings
from libs.html_template import HTMLTEMPLATE
from config_data import CONFIG

class Config(HTMLTEMPLATE):
    '''Config'''

    @cherrypy.expose
    def index(self, **kwargs) -> str:
        '''Config System'''
        print("CONFIG", kwargs, cherrypy.request.method)
        AUTHENTICATION.check_auth()
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPError(status=401)
        if kwargs:
            print("SAVE HTML")
            post_config_settings(kwargs)
            try:
                CONFIG.save()
            except OSError:
                print("ERROR WRITING CONFIG FILE")
        index_page = CONFIG.html()
        javascript = "config/javascript"
        return self._template(index_page, javascript=javascript)


    @cherrypy.expose
    def javascript(self) -> str:
        '''Javascript File'''
        return str(open("www/javascript/config.js", "r").read())
