'''HTML Systems'''
from typing import Any
import os
import re


class HTMLSystem:
    '''HTML Systems'''

    @classmethod
    def open(cls, file: str, extension: str = "html") -> str:
        '''opens the file and returns it'''
        return str(open(f"{os.getcwd()}/www/html/{file}.{extension}", "r").read())

    @classmethod
    def part(cls, file: str, **kwargs: Any) -> str:
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
