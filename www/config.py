'''Script For the Config System'''
import cherrypy
# from libs import html_parts
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE
# from libs.config import full_config_page, get_config_multi_setup, post_config_settings
from libs.root_event import RootEvent
from config_data import CONFIG
from libs.authenticator import AUTHENTICATION

class Config(HTMLTEMPLATE):
    '''Config'''

    @cherrypy.expose
    def index(self, **kwargs) -> str:
        '''Config System'''
        AUTHENTICATION.check_auth()
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPError(status=401)
        # if kwargs:
        #     post_config_settings(kwargs, self._tackem_system.config(),
        #                          self._tackem_system.plugins())
        #     try:
        #         CONFIG.save()
        #     except OSError:
        #         print("ERROR WRITING CONFIG FILE")
        #     RootEvent.set_event("reboot")
        #     page = str(open("www/html/reboot.html", "r").read())
        #     page = page.replace("%%PAGE%%", "")
        #     return self._template(page, False)
        index_page = full_config_page(self._tackem_system.config(), self._tackem_system.plugins())
        javascript = "config_javascript"
        return self._template(index_page, javascript=javascript)


    @cherrypy.expose
    def config_javascript(self) -> str:
        '''Javascript File'''
        return str(open("www/javascript/config.js", "r").read())


    @cherrypy.expose
    def get_multi_setup(self, **kwargs) -> str:
        '''Return the information needed for the setup of the plugin'''
        if kwargs:
            plugin = kwargs.get("plugin")
            name = kwargs.get("name", "")
            return get_config_multi_setup(self._tackem_system.plugins(), plugin,
                                          self._tackem_system.config(), name)
        raise cherrypy.HTTPError(status=404)
