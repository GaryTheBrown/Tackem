'''HTML Systems'''
import os

class HTMLSystem:
    '''HTML Systems'''


    __root = "www/html/"
    __theme = "default"


    @classmethod
    def __location(cls, file: str = "") -> str:
        '''creates the location'''
        return cls.__root + cls.__theme + "/" + file + ".html"


    @classmethod
    def open(cls, file: str) -> str:
        '''opens the file and returns it'''
        return str(open(cls.__location(file), "r").read())


    @classmethod
    def change_template(cls, theme: str) -> str:
        '''Changes the template being used'''
        themes = next(os.walk(cls.__root))[1]
        if theme in themes:
            cls.__theme = theme
            return True
        return False


    @classmethod
    def part(cls, file: str, **kwargs) -> str:
        '''All in one html template sorter'''
        html = cls.open(file)

        for key, arg in kwargs.items():
            html = html.replace("%%" + str(key).upper() + "%%", str(arg))
        return html
