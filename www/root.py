'''Script For the Root Of The System'''
import cherrypy
from libs import html_parts
from libs.html_template import HTMLTEMPLATE
from libs.config import full_config_page, get_config_multi_setup, post_config_settings
from libs.root_event import RootEvent

class Root(HTMLTEMPLATE):
    '''Root'''


    @cherrypy.expose
    def index(self) -> str:
        '''Index Page'''
        # self._tackem_system.auth.check_auth()
        index_page = str(open("www/html/pages/homepage.html", "r").read())

        return self._template(index_page)


    @cherrypy.expose
    def about(self) -> str:
        '''About Page'''
        index_page = str(open("www/html/pages/about.html", "r").read())

        return self._template(index_page)


    @cherrypy.expose
    def config(self, **kwargs) -> str:
        '''Config System'''
        self._tackem_system.auth.check_auth()
        if not self._tackem_system.auth.is_admin():
            raise cherrypy.HTTPError(status=401)
        if kwargs:
            post_config_settings(kwargs, self._tackem_system.config(),
                                 self._tackem_system.plugins())
            try:
                self._tackem_system.config().write()
            except OSError:
                print("ERROR WRITING CONFIG FILE")
            RootEvent.set_event("reboot")
            page = str(open("www/html/reboot.html", "r").read())
            page = page.replace("%%PAGE%%", "")
            return self._template(page, False)
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


    @cherrypy.expose
    def login(self, **kwargs) -> str:
        '''Login Page'''
        return_url = kwargs.get('return_url', "%%BASEURL%%")
        username = kwargs.get('username', "")
        password = kwargs.get('password', "")
        timeout = kwargs.get('timeout', "")
        if username != "" and password != "":
            self._tackem_system.auth.login(username, password, timeout, return_url)
        login_page = html_parts.login_page(return_url)
        return self._template(login_page, navbar=False)


    @cherrypy.expose
    def password(self, **kwargs) -> str:
        '''Login Page'''
        self._tackem_system.auth.check_auth()
        password_page = html_parts.password_page()
        password = kwargs.get('password', None)
        new_password = kwargs.get('new_password', None)
        new_password_check = kwargs.get('new_password_check', None)
        if password is not None and new_password is not None and new_password_check is not None:
            if new_password == new_password_check:
                if self._tackem_system.auth.change_password(password, new_password):
                    raise cherrypy.HTTPRedirect(cherrypy.url().replace("/password", "/"))
        return self._template(password_page, navbar=False)


    @cherrypy.expose
    def logout(self) -> None:
        '''Logout Page'''
        self._tackem_system.auth.logout()


    @cherrypy.expose
    def reboot(self, url: str = "login") -> str:
        '''Login Page'''
        if not self._tackem_system.auth.is_admin():
            raise cherrypy.HTTPError(status=401)
        RootEvent.set_event("reboot")
        page = str(open("www/html/reboot.html", "r").read())
        page = page.replace("%%PAGE%%", url)
        return self._template(page, False)


    @cherrypy.expose
    def shutdown(self) -> str:
        '''Login Page'''
        if not self._tackem_system.auth.is_admin():
            raise cherrypy.HTTPError(status=401)
        RootEvent.set_event("shutdown")
        page = "Shuting Down Tackem..."
        return self._template(page, False)


    @cherrypy.expose
    def restart(self) -> str:
        '''Restarts Tackem'''
        if not self._tackem_system.auth.is_admin():
            raise cherrypy.HTTPError(status=401)
        try:
            self._tackem_system.config().write()
        except OSError:
            print("ERROR WRITING CONFIG FILE")
        RootEvent.set_event("reboot")
        return ""
