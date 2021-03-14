"""Script For the Root Of The System"""
from typing import Any
import cherrypy
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE
from libs.authenticator import Authentication


class Root(HTMLTEMPLATE):
    """Root"""

    @cherrypy.expose
    def index(self) -> str:
        """Index Page"""
        Authentication.check_auth()
        return self._template(HTMLSystem.open("pages/homepage"))

    @cherrypy.expose
    def about(self) -> str:
        """About Page"""
        return self._template(HTMLSystem.open("pages/about"))

    @cherrypy.expose
    def login(self, **kwargs: Any) -> str:
        """Login Page"""
        return_url = kwargs.get("return_url", "%%BASEURL%%")
        username = kwargs.get("username", "")
        password = kwargs.get("password", "")
        timeout = kwargs.get("timeout", "")
        if username != "" and password != "":
            Authentication.login(username, password, timeout, return_url)

        return self._template(HTMLSystem.part("pages/login", RETURNURL=return_url), navbar=False)

    @cherrypy.expose
    def password(self, **kwargs: Any) -> str:
        """Login Page"""
        Authentication.check_auth()
        password = kwargs.get("password", None)
        new_password = kwargs.get("new_password", None)
        new_password_check = kwargs.get("new_password_check", None)
        if password is not None and new_password is not None and new_password_check is not None:
            if new_password == new_password_check:
                if Authentication.change_password(password, new_password):
                    raise cherrypy.HTTPRedirect(cherrypy.url().replace("/password", "/"))
        return self._template(HTMLSystem.part("pages/password"), navbar=False)

    @cherrypy.expose
    def logout(self):
        """Logout Page"""
        Authentication.logout()
