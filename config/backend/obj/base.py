"""Shared Data for all config Objects"""
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Optional

from config.backend.base import ConfigBase
from config.backend.obj.data.data_list import DataList
from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.rules import ConfigRules


class ConfigObjBase(ABC, ConfigBase):
    """Shared Data for all config Objects"""

    def __init__(
        self,
        var_name: str,
        default_value: Any,
        label: str,
        help_text: str,
        hide_on_html: bool = False,
        not_in_config: bool = False,
        rules: Optional[ConfigRules] = None,
        input_attributes: Optional[InputAttributes] = None,
        data_list: Optional[DataList] = None,
        value_link: Optional[list] = None,
    ):
        super().__init__(var_name, label, help_text, hide_on_html, not_in_config, rules, value_link)
        if input_attributes and not isinstance(input_attributes, InputAttributes):
            raise ValueError("input_attributes not correct type")
        if data_list and not isinstance(data_list, DataList):
            raise ValueError("data_list not correct type")

        self.__value = default_value
        self.__default_value = default_value
        self.__input_attributes = input_attributes
        self.__data_list = data_list

    @property
    def value(self):
        """returns the value"""
        return self.__value

    @value.setter
    def value(self, value: Any):
        """sets the value"""
        self.__value = self._set_value(value)

    @abstractmethod
    def _set_value(self, value):
        """hidden abstract method for setting the value with checking of type in sub classes"""

    @property
    def default_value(self):
        """returns the default value"""
        return self.__default_value

    @property
    def input_attributes(self) -> Optional[InputAttributes]:
        """returns the input attributes"""
        return self.__input_attributes

    @property
    def data_list(self) -> Optional[DataList]:
        """returns the data list"""
        return self.__data_list

    @property
    @abstractmethod
    def spec(self) -> str:
        """Returns the line for the config option"""

    def to_type(self, value: Any):
        """returns the value in the correct format"""
        return value

    def reset_value_to_default(self):
        """returns the value back to default"""
        self.__value = self.__default_value

    @abstractmethod
    def html_dict(self, variable_name: str) -> dict:
        """returns the required Data for the html template to use"""
        return_dict = {
            "value": self.__value,
            "default_value": self.__default_value,
        }

        return_dict.update(ConfigBase.html_dict(self, variable_name))

        if isinstance(self.input_attributes, InputAttributes):
            return_dict["input_attributes"] = self.input_attributes.html()

        if self.__data_list and isinstance(self.__data_list, DataList):
            return_dict["data_list"] = self.__data_list.html_dict(variable_name)

        return return_dict
