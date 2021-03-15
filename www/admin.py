"""Script For the Admin System"""
from typing import Any

import cherrypy

from data.config import CONFIG
from libs.authenticator import Authentication
from libs.config.list import ConfigList
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE


class Admin(HTMLTEMPLATE):
    """Admin"""

    @cherrypy.expose
    def config(self, **kwargs: Any) -> str:
        """CONFIG System"""
        Authentication.check_auth()
        if not Authentication.is_admin():
            raise cherrypy.HTTPError(status=401)
        if kwargs:
            for key, value in kwargs.items():
                key = key.replace("[]", "")
                key_list = key.split("_")
                self.__add_val_to_config(key, CONFIG, key_list, value)
            try:
                CONFIG.save()
            except OSError:
                print("ERROR WRITING Config FILE")
        return self._template(CONFIG.html(), javascript="js/config.js")

    @cherrypy.expose
    def users(self) -> str:
        """Grab the users info"""
        Authentication.check_auth()
        if not Authentication.is_admin():
            raise cherrypy.HTTPError(status=401)
        data = Authentication.get_users()
        users_html = ""
        for item in data:
            admin = "checked" if item["is_admin"] else ""
            admin += " disabled" if item["id"] == 1 else ""
            users_html += HTMLSystem.part(
                "section/user", USERID=item["id"], NAME=item["username"], ISADMIN=admin
            )
        return self._template(
            HTMLSystem.part("pages/users", USERSHTML=users_html),
            javascript="js/users.js",
        )

    @cherrypy.expose
    def shutdown(self) -> str:
        """shutdown the system page"""
        Authentication.check_auth()
        if not Authentication.is_admin():
            raise cherrypy.HTTPError(status=401)
        return self._template(HTMLSystem.part("pages/shutdown"))

    @cherrypy.expose
    def reboot(self) -> str:
        """reboot the system page"""
        Authentication.check_auth()
        if not Authentication.is_admin():
            raise cherrypy.HTTPError(status=401)
        return self._template(HTMLSystem.part("pages/reboot"))

    def __add_val_to_config(self, key: str, config: ConfigList, key_list: list, value: Any):
        """recursive way of adding value into the config"""
        if len(key_list) == 1:
            if key_list[0] in config.keys():
                config[key_list[0]].value = value
                return

            for obj in config:
                if isinstance(obj, ConfigList) and obj.is_section:
                    if key_list[0] in obj.keys():
                        obj[key_list[0]].value = value
                        return
        else:
            if config.many_section:
                config.clone_many_section(key_list[0])

            if key_list[0] in config.keys():
                return self.__add_val_to_config(key, config[key_list[0]], key_list[1:], value)

            for obj in config:
                if obj.is_section:
                    return self.__add_val_to_config(key, obj, key_list, value)
