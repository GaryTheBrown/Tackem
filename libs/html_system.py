'''HTML Systems'''
import os
from libs.startup_arguments import THEMEFOLDERLOCATION

class HTMLSystem:
    '''HTML Systems'''


    __theme = "default"


    @classmethod
    def set_theme(cls, theme: str):
        '''sets the theme as cannot directly access the config due to circular dependency'''
        cls.__theme = theme


    @classmethod
    def __location(cls, file: str, extension: str) -> str:
        '''creates the location'''
        location = THEMEFOLDERLOCATION + cls.__theme
        location += "/html/" + file + "." + extension
        return location


    @classmethod
    def open(cls, file: str, extension: str = "html") -> str:
        '''opens the file and returns it'''
        return str(open(cls.__location(file, extension), "r").read())


    @classmethod
    def part(cls, file: str, **kwargs) -> str:
        '''All in one html template sorter'''
        html = cls.open(file)

        for key, arg in kwargs.items():
            html = html.replace("%%" + str(key).upper() + "%%", str(arg))
        return html

    @staticmethod
    @property
    def theme_list():
        '''returns list of themes'''
        return next(os.walk(THEMEFOLDERLOCATION))[1]
