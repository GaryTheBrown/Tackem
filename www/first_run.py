'''Script For the first Run Of The System'''
import cherrypy
from libs.html_template import HTMLTEMPLATE
from libs.config import post_config_settings, plugin_config_page
from libs.config import root_config_page, get_config_multi_setup
from libs.config import javascript as config_javascript
from libs.root_event import RootEvent
from libs import plugin_downloader

class Root(HTMLTEMPLATE):
    '''Setup Script'''
    @cherrypy.expose
    def index(self, **kwargs):
        '''Index Page'''
        if cherrypy.request.method == "POST" and kwargs:
            if "page_index" in kwargs:
                return self._post_action(kwargs)

        page = str(open("www/html/pages/firstrunindex.html", "r").read())
        return self._template(page, False)

    @cherrypy.expose
    def javascript(self):
        '''Javascript File'''
        return config_javascript()

    @cherrypy.expose
    def plugin_downloader_javascript(self):
        '''Javascript File'''
        return plugin_downloader.javascript()

    @cherrypy.expose
    def get_multi_setup(self, plugin, name=""):
        '''Return the information needed for the setup of the plugin'''
        return get_config_multi_setup(self._tackem_system.plugins(), plugin,
                                      self._tackem_system.config(), name)

    def _post_action(self, kwargs):
        '''the part of the script to do all of the pages & updates of the config'''
        post_config_settings(kwargs, self._tackem_system.config(), self._tackem_system.plugins())
        try:
            self._tackem_system.config().write()
        except OSError:
            print("ERROR WRITING CONFIG FILE")
        javascript = "javascript"
        plugin_downloader_javascript = "plugin_downloader_javascript"
        if kwargs["page_index"] == "1":
            return self._template(root_config_page(self._tackem_system.config()), False,
                                  javascript=javascript)
        if kwargs["page_index"] == "2":
            return self._template(plugin_downloader.plugin_download_page(False),
                                  False, javascript=plugin_downloader_javascript)
        if kwargs["page_index"] == "3":
            return self._template(plugin_config_page(self._tackem_system.config(),
                                                     self._tackem_system.plugins()),
                                  False, javascript=javascript)
        if kwargs["page_index"] == "4":
            self._tackem_system.set_config(['firstrun'], False)
            try:
                self._tackem_system.config().write()
            except OSError:
                print("ERROR WRITING CONFIG FILE")
            RootEvent.set_event("reboot")
            page = str(open("www/html/reboot.html", "r").read())
            page = page.replace("%%PAGE%%", "login")
            return self._template(page, False)
        return self._template("TODO", False)

    @cherrypy.expose
    def download_plugin(self, name):
        '''download the plugin program link'''
        return str(plugin_downloader.download_plugin(name)).lower()

    @cherrypy.expose
    def remove_plugin(self, name):
        '''remove the plugin program link'''
        plugin_downloader.delete_plugin(name)
        return "true"

    @cherrypy.expose
    def restart(self):
        '''Restarts Tackem'''
        try:
            self._tackem_system.config().write()
        except OSError:
            print("ERROR WRITING CONFIG FILE")
        RootEvent.set_event("reboot")
        return ""
