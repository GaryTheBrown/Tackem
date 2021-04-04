"""Script For the Admin System"""
from typing import Any

import cherrypy

from data.config import CONFIG
from libs.authentication import Authentication
from libs.config.list import ConfigList


class Admin:
    """Admin"""

    @cherrypy.tools.template(user=Authentication.ADMIN)
    def config(self, **kwargs: Any) -> dict:
        """CONFIG System"""
        if kwargs:
            for key, value in kwargs.items():
                key = key.replace("[]", "")
                key_list = key.split("_")
                self.__add_val_to_config(key, CONFIG, key_list, value)
            try:
                CONFIG.save()
            except OSError:
                print("ERROR WRITING Config FILE")
        config_dict = CONFIG.html_dict()
        return {"config": config_dict}

    @cherrypy.tools.template(user=Authentication.ADMIN)
    def users(self) -> dict:
        """Grab the users info"""
        return {"users": Authentication.get_users()}

    @cherrypy.tools.template(user=Authentication.ADMIN)
    def shutdown(self) -> dict:
        """shutdown the system page"""

    @cherrypy.tools.template(user=Authentication.ADMIN)
    def reboot(self) -> dict:
        """reboot the system page"""

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
                if isinstance(obj, ConfigList) and obj.is_section:
                    return self.__add_val_to_config(key, obj, key_list, value)

        print("VAR FAILED:", key, key_list, value)
