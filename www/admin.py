'''Script For the Admin System'''
import cherrypy
from typing import Any
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE
from libs.authenticator import Authentication
from libs.config.html.post_to_config import post_config_settings
from data.config import CONFIG

class Admin(HTMLTEMPLATE):
    '''Admin'''

    @cherrypy.expose
    def config(self, **kwargs: Any) -> str:
        '''CONFIG System'''
        Authentication.check_auth()
        if not Authentication.is_admin():
            raise cherrypy.HTTPError(status=401)
        if kwargs:
            post_config_settings(kwargs)
            try:
                CONFIG.save()
            except OSError:
                print("ERROR WRITING Config FILE")
        return self._template(CONFIG.html(), javascript="static/js/config.js")

    @cherrypy.expose
    def users(self) -> str:
        '''Grab the users info'''
        Authentication.check_auth()
        if not Authentication.is_admin():
            raise cherrypy.HTTPError(status=401)
        data = Authentication.get_users()
        users_html = ""
        for item in data:
            admin = "checked" if item['is_admin'] else ""
            admin += " disabled" if item['id'] == 1 else ""
            users_html += HTMLSystem.part(
                "section/user",
                USERID=item['id'],
                NAME=item['username'],
                ISADMIN=admin
            )
        return self._template(
            HTMLSystem.part(
                "pages/users",
                USERSHTML=users_html
            ),
            javascript="static/js/users.js"
        )

    @cherrypy.expose
    def shutdown(self) -> str:
        '''shutdown the system page'''
        Authentication.check_auth()
        if not Authentication.is_admin():
            raise cherrypy.HTTPError(status=401)
        return self._template(
            HTMLSystem.part(
                "pages/shutdown"
            )
        )

    @cherrypy.expose
    def reboot(self) -> str:
        '''reboot the system page'''
        Authentication.check_auth()
        if not Authentication.is_admin():
            raise cherrypy.HTTPError(status=401)
        return self._template(
            HTMLSystem.part(
                "pages/reboot"
            )
        )
