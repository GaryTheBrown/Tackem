'''Script For the Root Of The System'''
import cherrypy
from libs import html_parts
from libs.html_template import HTMLTEMPLATE
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
        index_page = str(open("www/html/pages/welcome.html", "r").read())
        return self._template(index_page)

    @cherrypy.expose
    def index(self):
        '''Index Page'''
        self._auth.check_auth()
        index_page = str(open("www/html/pages/homepage.html", "r").read())

        return self._template(index_page)

    @cherrypy.expose
    def config(self, **kwargs):
        '''Config System'''
        if self._auth.enabled():
            self._auth.check_auth()
            if not self._auth.is_admin():
                return self._error_page(401)
        if kwargs:
            post_config_settings(kwargs, self._global_config, self._plugins)
            try:
                self._global_config.write()
            except OSError:
                print("ERROR WRITING CONFIG FILE")
            RootEvent().set_event("reboot")
            page = str(open("www/html/reboot.html", "r").read())
            page = page.replace("%%PAGE%%", "")
            return self._template(page, False)
        index_page = full_config_page(self._global_config, self._plugins)
        javascript = "config_javascript"
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
            return get_config_multi_setup(self._plugins, plugin, self._global_config, name)
        return "ERROR YOU SHOULD NOT BE HERE"

    @cherrypy.expose
    def login(self, **kwargs):
        '''Login Page'''
        if not self._auth.enabled():
            raise cherrypy.HTTPRedirect(cherrypy.url().replace("/login", "/"))
        return_url = kwargs.get('return_url', "%%BASEURL%%")
        username = kwargs.get('username', "")
        password = kwargs.get('password', "")
        timeout = kwargs.get('timeout', "")
        if username != "" and password != "":
            self._auth.login(username, password, timeout, return_url)
        login_page = html_parts.login_page(return_url)
        return self._template(login_page, navbar=False)

    @cherrypy.expose
    def password(self, **kwargs):
        '''Login Page'''
        if not self._auth.enabled():
            raise cherrypy.HTTPRedirect(cherrypy.url().replace("/password", "/"))
        self._auth.check_auth()
        password_page = html_parts.password_page()
        password = kwargs.get('password', None)
        new_password = kwargs.get('new_password', None)
        new_password_check = kwargs.get('new_password_check', None)
        if password is not None and new_password is not None and new_password_check is not None:
            if new_password == new_password_check:
                if self._auth.change_password(password, new_password):
                    raise cherrypy.HTTPRedirect(cherrypy.url().replace("/password", "/"))
        return self._template(password_page, navbar=False)

    @cherrypy.expose
    def logout(self):
        '''Logout Page'''
        if not self._auth.enabled():
            raise cherrypy.HTTPRedirect(cherrypy.url().replace("/logout", "/"))
        self._auth.logout()

    @cherrypy.expose
    def reboot(self):
        '''Login Page'''
        if self._auth.enabled():
            if not self._auth.is_admin():
                return self._error_page(401)
        RootEvent().set_event("reboot")
        page = str(open("www/html/reboot.html", "r").read())
        page = page.replace("%%PAGE%%", "login")
        return self._template(page, False)

    @cherrypy.expose
    def shutdown(self):
        '''Login Page'''
        if self._auth.enabled():
            if not self._auth.is_admin():
                return self._error_page(401)
        RootEvent().set_event("shutdown")
        page = "Shuting Down Tackem..."
        return self._template(page, False)
