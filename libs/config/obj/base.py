'''Shared Data for all config Objects'''
from typing import Optional
from abc import ABC, abstractmethod
from libs.config.base import ConfigBase
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.data_list import DataList
from libs.config.rules import ConfigRules
from libs.html_system import HTMLSystem

#http://www.voidspace.org.uk/python/validate.html
class ConfigObjBase(ABC, ConfigBase):
    '''Shared Data for all config Objects'''



    __configobj_types = [
        "pass", "string", "float", "string_list", "boolean", "option", "integer", "password",
        "ip_addr", "list", "force_list", "tuple", "int_list", "float_list", "bool_list",
        "ip_addr_list", "mixed_list"
    ]

    __input_types = [
        "button", "checkbox", "color", "date", "datetime-local", "email", "file", "hidden", "image",
        "month", "number", "password", "radio", "range", "reset", "search", "submit", "tel", "text",
        "time", "url", "week"
    ]

    __form_attributes = [
        "autocomplete", "novalidate"
    ]

    __input_attributes = [
        "value", "readonly", "disabled", "size", "maxlength", "autocomplete", "autofocus", "form",
        "formaction", "formenctype", "formmethod", "formnovalidate", "formtarget", "height",
        "width", "list", "min", "max", "multiple", "pattern", "placeholder", "required", "step",
        "alt"
    ]

    __html_types = [
        "input", "select", "multiselect", "textarea", "button", "datalist",
    ]

    _special_html = [
        "fieldset", "legend",
    ]

    _select_extras = [
        "option",
        "optgroup",
    ]


    def __init__(
            self,
            var_name: str,
            default_value,
            label: str,
            help_text: str,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            rules: Optional[ConfigRules] = None,
            input_attributes: Optional[InputAttributes] = None,
            data_list: Optional[DataList] = None
    ):
        super().__init__(
            var_name,
            label,
            help_text,
            hide_on_html,
            not_in_config,
            rules
        )
        if input_attributes and not isinstance(input_attributes, InputAttributes):
            raise ValueError("input_attributes not correct type")
        if data_list and not isinstance(data_list, DataList):
            raise ValueError("data_list not correct type")

        self.__value = default_value
        self.__default_value = default_value
        self.__input_attributes = None
        self.__data_list = None
        self.__input_attributes = input_attributes
        self.__data_list = data_list


    @property
    def value(self):
        '''returns the value'''
        return self.__value


    @value.setter
    def value(self, value):
        '''sets the value'''
        self.__value = value


    @property
    def default_value(self):
        '''returns the default value'''
        return self.__default_value


    @property
    def input_attributes(self) -> Optional[InputAttributes]:
        '''returns the input attributes'''
        return self.__input_attributes


    @property
    def data_list(self) -> Optional[DataList]:
        '''returns the data list'''
        return self.__data_list


    @property
    @abstractmethod
    def spec(self) -> str:
        '''Returns the line for the config option'''


    @abstractmethod
    def item_html(self, variable_name: str, value) -> str:
        '''Returns the html for the config option'''

    def to_type(self, value):
        '''returns the value in the correct format'''
        return value


    @property
    def html(self, variable_name: str, value) -> str:
        '''returns the full html code including label and help text'''
        if self.hide_on_html:
            return ""
        return HTMLSystem.part(
            "sections/item",
            VARNAME=self.var_name,
            LABEL=self.label,
            HELP=self.help_text,
            INPUT=self.item_html(variable_name, value)
        )

    def reset_value_to_default(self):
        '''returns the value back to default'''
        self.__value = self.__default_value
