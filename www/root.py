'''Script For the Root Of The System'''
import cherrypy
# from libs import html_parts
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE
# from libs.config import full_config_page, get_config_multi_setup, post_config_settings
from libs.root_event import RootEvent
from libs.authenticator import AUTHENTICATION
from config_data import CONFIG

class Root(HTMLTEMPLATE):
    '''Root'''


    @cherrypy.expose
    def index(self) -> str:
        '''Index Page'''
        AUTHENTICATION.check_auth()

        return self._template(HTMLSystem.open("pages/homepage"))


    @cherrypy.expose
    def about(self) -> str:
        '''About Page'''
        return self._template(HTMLSystem.open("pages/about"))

    @cherrypy.expose
    def stylesheet(self) -> str:
        '''Javascript File'''
        return HTMLSystem.open("style", "css")

    @cherrypy.expose
    def login(self, **kwargs) -> str:
        '''Login Page'''
        return_url = kwargs.get('return_url', "%%BASEURL%%")
        username = kwargs.get('username', "")
        password = kwargs.get('password', "")
        timeout = kwargs.get('timeout', "")
        if username != "" and password != "":
            AUTHENTICATION.login(username, password, timeout, return_url)

        return self._template(HTMLSystem.part("pages/login", RETURNURL=return_url), navbar=False)


    @cherrypy.expose
    def password(self, **kwargs) -> str:
        '''Login Page'''
        AUTHENTICATION.check_auth()
        password = kwargs.get('password', None)
        new_password = kwargs.get('new_password', None)
        new_password_check = kwargs.get('new_password_check', None)
        if password is not None and new_password is not None and new_password_check is not None:
            if new_password == new_password_check:
                if AUTHENTICATION.change_password(password, new_password):
                    raise cherrypy.HTTPRedirect(cherrypy.url().replace("/password", "/"))
        return self._template(HTMLSystem.part("pages/password"), navbar=False)


    @cherrypy.expose
    def logout(self) -> None:
        '''Logout Page'''
        AUTHENTICATION.logout()


    @cherrypy.expose
    def reboot(self, url: str = "login") -> str:
        '''Login Page'''
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPError(status=401)
        RootEvent.set_event("reboot")
        return self._template(HTMLSystem.part("reboot", PAGE=url), False)


    @cherrypy.expose
    def shutdown(self) -> str:
        '''Login Page'''
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPError(status=401)
        RootEvent.set_event("shutdown")
        return self._template("Shuting Down Tackem...", False)


    @cherrypy.expose
    def restart(self) -> str:
        '''Restarts Tackem'''
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPError(status=401)
        try:
            CONFIG.save()
        except OSError:
            print("ERROR WRITING CONFIG FILE")
        RootEvent.set_event("reboot")
        return ""
