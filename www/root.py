'''Script For the Root Of The System'''
import cherrypy
from libs.htmltemplate import HTMLTEMPLATE
from libs.config import full_config_page, get_config_multi_setup, post_config_settings
from libs.config import javascript as config_javascript
from libs.root_event import RootEvent

class Root(HTMLTEMPLATE):
    '''Root'''

    @cherrypy.expose
    def welcome(self, **kwargs):
        '''First Run Will Load Into this page'''
        if kwargs:
            #first startup message add here
            pass
        index_page = str(open("www/html/welcome.html", "r").read())
        return self._template(index_page)

    @cherrypy.expose
    def index(self):
        '''Index Page'''
        index_page = str(open("www/html/homepage.html", "r").read())

        return self._template(index_page)

    @cherrypy.expose
    def config(self, **kwargs):
        '''Config System'''
        if kwargs:
            post_config_settings(kwargs, self._config, self._plugins)
            try:
                self._config.write()
            except OSError:
                print("ERROR WRITING CONFIG FILE")
            RootEvent().set_event("reboot")
            page = str(open("www/html/reboot.html", "r").read())
            return self._template(page, False)
        index_page = full_config_page(self._config, self._plugins)
        javascript = self._config.get("webui", {}).get("baseurl", "") + "/config_javascript"
        return self._template(index_page, javascript=javascript)

    @cherrypy.expose
    def config_javascript(self):
        '''Javascript File'''
        return config_javascript()

    @cherrypy.expose
    def get_multi_setup(self, **kwargs):
        '''Return the information needed for the setup of the plugin'''
        if kwargs:
            plugin = kwargs.get("plugin")
            name = kwargs.get("name", "")
            return get_config_multi_setup(self._plugins, plugin, self._config, name)
        return "ERROR YOU SHOULD NOT BE HERE"
