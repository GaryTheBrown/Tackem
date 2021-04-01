"""Script For the Root Of The System"""
from typing import Any

import cherrypy

from data.config import CONFIG
from libs.authentication import Authentication
from libs.ripper import Ripper as RipperSYS
from www.controller.admin import Admin
from www.controller.ripper import Ripper
from www.controller.upload import Upload


class Root:
    """Root"""

    admin = None
    ripper = None
    upload = None

    def __init__(self):
        self.admin = Admin()
        self.upload = Upload()
        if RipperSYS.enabled:
            self.ripper = Ripper()

    @cherrypy.tools.template(user=Authentication.USER)
    def index(self):
        """Index Page"""

    @cherrypy.tools.template
    def about(self):
        """About Page"""

    @cherrypy.tools.template
    def login(self, **kwargs: Any):
        """Login Page"""
        return_url = kwargs.get("return_url", CONFIG["webui"]["baseurl"].value)
        username = kwargs.get("username", "")
        password = kwargs.get("password", "")
        timeout = kwargs.get("timeout", "")
        if len(username) > 0 and len(password) > 0:
            Authentication.login(username, password, timeout, return_url)
        return {"returnurl": return_url}

    @cherrypy.tools.template(user=Authentication.USER)
    def password(self, **kwargs: Any):
        """Login Page"""
        Authentication.check_auth()
        password = kwargs.get("password", None)
        new_password = kwargs.get("new_password", None)
        new_password_check = kwargs.get("new_password_check", None)
        if password is not None and new_password is not None and new_password_check is not None:
            if new_password == new_password_check:
                if Authentication.change_password(password, new_password):
                    raise cherrypy.HTTPRedirect(cherrypy.url().replace("/password", "/"))

    @cherrypy.expose
    def logout(self):
        """Logout Page"""
        Authentication.logout()
