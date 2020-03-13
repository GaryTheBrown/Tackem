'''Config Object Data List'''
from libs.html_system import HTMLSystem


class DataList:
    '''Config Object Data List'''

    def __init__(self, variable_name, *options):
        if not isinstance(variable_name, str):
            raise ValueError("variable name is not a String")
        if not all([isinstance(x, DataListOption) for x in options]):
            raise ValueError(
                "One of the Data List Options is not the right Type of Class")

        self.__variable_name = variable_name
        self.__options = options

    @property
    def html(self):
        '''returns the data in html form'''
        return HTMLSystem.part(
            "input/datalist",
            VARNAME=self.__variable_name,
            OPTIONS="".join([x.html for x in self.__options])
        )


class DataListOption:
    '''Config Object Data List Option'''

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Value is not a String")
        self.__value = value

    @property
    def html(self):
        '''returns the data in html form'''
        return HTMLSystem.part(
            "input/datalistoption",
            VALUE=self.__value
        )
