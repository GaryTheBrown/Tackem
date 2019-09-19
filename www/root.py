'''Script For the Root Of The System'''
import cherrypy
from libs import html_parts
from libs.html_template import HTMLTEMPLATE
from libs.config import full_config_page, get_config_multi_setup, post_config_settings
from libs.config import javascript as config_javascript
from libs.root_event import RootEvent
from libs import plugin_downloader

class Root(HTMLTEMPLATE):
    '''Root'''

    @cherrypy.expose
    def index(self):
        '''Index Page'''
        # self._tackem_system.get_auth().check_auth()
        index_page = str(open("www/html/pages/homepage.html", "r").read())

        return self._template(index_page)

    @cherrypy.expose
    def about(self):
        '''About Page'''
        index_page = str(open("www/html/pages/about.html", "r").read())

        return self._template(index_page)
    @cherrypy.expose
    def config(self, **kwargs):
        '''Config System'''
        self._tackem_system.get_auth().check_auth()
        if not self._tackem_system.get_auth().is_admin():
            return self._error_page(401)
        if kwargs:
            post_config_settings(kwargs, self._tackem_system.config(),
                                 self._tackem_system.plugins())
            try:
                self._tackem_system.config().write()
            except OSError:
                print("ERROR WRITING CONFIG FILE")
            RootEvent().set_event("reboot")
            page = str(open("www/html/reboot.html", "r").read())
            page = page.replace("%%PAGE%%", "")
            return self._template(page, False)
        index_page = full_config_page(self._tackem_system.config(), self._tackem_system.plugins())
        javascript = "config_javascript"
        return self._template(index_page, javascript=javascript)

    @cherrypy.expose
    def config_javascript(self):
        '''Javascript File'''
        return config_javascript()

    @cherrypy.expose
    def plugin_downloader_javascript(self):
        '''Javascript File'''
        return plugin_downloader.javascript()

    @cherrypy.expose
    def get_multi_setup(self, **kwargs):
        '''Return the information needed for the setup of the plugin'''
        if kwargs:
            plugin = kwargs.get("plugin")
            name = kwargs.get("name", "")
            return get_config_multi_setup(self._tackem_system.plugins(), plugin,
                                          self._tackem_system.config(), name)
        return "ERROR YOU SHOULD NOT BE HERE"

    @cherrypy.expose
    def login(self, **kwargs):
        '''Login Page'''
        if not self._tackem_system.get_auth().enabled():
            raise cherrypy.HTTPRedirect(cherrypy.url().replace("/login", "/"))
        return_url = kwargs.get('return_url', "%%BASEURL%%")
        username = kwargs.get('username', "")
        password = kwargs.get('password', "")
        timeout = kwargs.get('timeout', "")
        if username != "" and password != "":
            self._tackem_system.get_auth().login(username, password, timeout, return_url)
        login_page = html_parts.login_page(return_url)
        return self._template(login_page, navbar=False)

    @cherrypy.expose
    def password(self, **kwargs):
        '''Login Page'''
        if not self._tackem_system.get_auth().enabled():
            raise cherrypy.HTTPRedirect(cherrypy.url().replace("/password", "/"))
        self._tackem_system.get_auth().check_auth()
        password_page = html_parts.password_page()
        password = kwargs.get('password', None)
        new_password = kwargs.get('new_password', None)
        new_password_check = kwargs.get('new_password_check', None)
        if password is not None and new_password is not None and new_password_check is not None:
            if new_password == new_password_check:
                if self._tackem_system.get_auth().change_password(password, new_password):
                    raise cherrypy.HTTPRedirect(cherrypy.url().replace("/password", "/"))
        return self._template(password_page, navbar=False)

    @cherrypy.expose
    def logout(self):
        '''Logout Page'''
        if not self._tackem_system.get_auth().enabled():
            raise cherrypy.HTTPRedirect(cherrypy.url().replace("/logout", "/"))
        self._tackem_system.get_auth().logout()

    @cherrypy.expose
    def reboot(self, url="login"):
        '''Login Page'''
        if self._tackem_system.get_auth().enabled():
            if not self._tackem_system.get_auth().is_admin():
                return self._error_page(401)
        RootEvent().set_event("reboot")
        page = str(open("www/html/reboot.html", "r").read())
        page = page.replace("%%PAGE%%", url)
        return self._template(page, False)

    @cherrypy.expose
    def shutdown(self):
        '''Login Page'''
        if self._tackem_system.get_auth().enabled():
            if not self._tackem_system.get_auth().is_admin():
                return self._error_page(401)
        RootEvent().set_event("shutdown")
        page = "Shuting Down Tackem..."
        return self._template(page, False)

    @cherrypy.expose
    def plugin_download(self):
        '''url for system access to plugin downloaded'''
        if self._tackem_system.get_auth().enabled():
            if not self._tackem_system.get_auth().is_admin():
                return self._error_page(401)
        javascript = "plugin_downloader_javascript"
        return self._template(plugin_downloader.plugin_download_page(True), False,
                              javascript=javascript)

    @cherrypy.expose
    def download_plugin(self, name):
        '''download the plugin program link'''
        if self._tackem_system.get_auth().enabled():
            if not self._tackem_system.get_auth().is_admin():
                return self._error_page(401)
        plugin_downloader.download_plugin(name)
        return html_parts.input_button("Remove",
                                       plugin_downloader.button_remove(name), False)

    @cherrypy.expose
    def remove_plugin(self, name):
        '''remove the plugin program link'''
        if self._tackem_system.get_auth().enabled():
            if not self._tackem_system.get_auth().is_admin():
                return self._error_page(401)
        plugin_downloader.delete_plugin(name)
        return html_parts.input_button("Add",
                                       plugin_downloader.button_add(name), False)

    @cherrypy.expose
    def restart(self):
        '''Restarts Tackem'''
        if self._tackem_system.get_auth().enabled():
            if not self._tackem_system.get_auth().is_admin():
                return self._error_page(401)
        try:
            self._tackem_system.config().write()
        except OSError:
            print("ERROR WRITING CONFIG FILE")
        RootEvent().set_event("reboot")
        return ""
