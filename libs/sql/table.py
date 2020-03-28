'''Database Table'''
from typing import List
from libs.sql.column import Column

class Table():
    '''Database Table'''

    def __init__(self, name: str, version: int, *data: List[Column]):
        self.__name = name
        self.__version = version
        self.__data = data

    def name(self, *values) -> str:
        '''returns the name'''
        if "{}" in self.__name and values is None:
            ValueError("Tried to get DB Name but missing values")
        if values:
            return self.__name.format(*values)
        return self.__name

    @property
    def version(self):
        '''returns the version'''
        return self.__version

    @property
    def data(self):
        '''returns data'''
        return self.__data
