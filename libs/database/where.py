"""Where Object"""
from typing import Any


class Where:
    """Where Object"""

    def __init__(self, key: str, value: Any, expression: str = "="):
        self.__key = key
        self.__value = value
        self.__expression = expression

    @property
    def key(self):
        """returns key"""
        return self.__key

    @property
    def value(self):
        """return value"""
        return self.__value

    @property
    def expression(self):
        """return expression"""
        return self.__expression

    @property
    def query(self):
        """returns the query String"""
        return f"{self.__key}{self.__expression}'{self.__value}'"
