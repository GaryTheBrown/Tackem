'''HTML Systems'''
from typing import Any
import os
import json
import re
from libs.startup_arguments import THEMEFOLDERLOCATION


class HTMLSystem:
    '''HTML Systems'''

    __theme = "default"
    __settings = {}
    __settings_defaults = {
        "post_save": True,
        "api_save": False,
    }

    @classmethod
    def set_theme(cls, theme: str):
        '''sets the theme as cannot directly access the config due to circular dependency'''
        cls.__theme = theme
        with open(cls.__location("settings", "json"), 'r') as json_file:
            cls.__settings = json.load(json_file)

    @classmethod
    def setting(cls, setting: str) -> Any:
        '''function to load the plugin settings.json'''
        if setting.lower() in cls.__settings_defaults:
            if setting.lower() in cls.__settings:
                return cls.__settings[setting.lower()]
            return cls.__settings_defaults[setting.lower()]
        return None

    @classmethod
    def __theme_location(cls) -> str:
        '''creates the location'''
        location = THEMEFOLDERLOCATION + cls.__theme + "/"
        return location

    @classmethod
    def __location(cls, file: str, extension: str) -> str:
        '''creates the location'''
        location = cls.__theme_location()
        location += file + "." + extension
        return location

    @classmethod
    def __html_location(cls, file: str, extension: str) -> str:
        '''creates the location'''
        location = cls.__theme_location()
        location += "html/" + file + "." + extension
        return location

    @classmethod
    def open(cls, file: str, extension: str = "html") -> str:
        '''opens the file and returns it'''
        return str(open(cls.__html_location(file, extension), "r").read())

    @classmethod
    def part(cls, file: str, **kwargs) -> str:
        '''All in one html template sorter'''
        html = cls.open(file)

        for key, arg in kwargs.items():
            html = html.replace("%%" + str(key).upper() + "%%", str(arg))

        regex = r"\%\%[A-Z0-9]*\%\%(?<!\%\%BASEURL\%\%)"
        for string in re.findall(regex, html):
            html = html.replace(string, "")

        return html

    @classmethod
    def script_link(cls, location: str) -> str:
        '''returns a script link item'''
        return cls.part(
            "tags/scriptlink",
            LOCATION=location
        )

    @classmethod
    def stylesheet_link(cls, location: str) -> str:
        '''returns a script link item'''
        return cls.part(
            "tags/stylesheetlink",
            LOCATION=location
        )

    @staticmethod
    @property
    def theme_list() -> list:
        '''returns list of themes'''
        return next(os.walk(THEMEFOLDERLOCATION))[1]
