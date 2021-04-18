"""Config Object Radios"""
from typing import Optional

from config.backend.obj.data.input_attributes import InputAttributes


class ConfigObjRadio:
    """Config Item Radios"""

    def __init__(
        self,
        value: str,
        label: str,
        hide_on_html: bool = False,
        not_in_config: bool = False,
        input_attributes: Optional[InputAttributes] = None,
    ):
        if not isinstance(value, str):
            raise ValueError("value is not a string")
        if not isinstance(label, str):
            raise ValueError("label is not a string")
        if not isinstance(hide_on_html, bool):
            raise ValueError("hide On HTML is not a bool")
        if not isinstance(not_in_config, bool):
            raise ValueError("not in config is not a bool")
        if input_attributes:
            if not isinstance(input_attributes, InputAttributes):
                raise ValueError("input_attributes not correct type")
            input_attributes.block("autofocus", "multiple", "required")

        self.__value = value
        self.__label = label
        self.__hide_on_html = hide_on_html
        self.__not_in_config = not_in_config
        self.__input_attributes = input_attributes

    @property
    def spec(self) -> str:
        """Returns the line for the config option"""
        if self.not_in_config:
            return ""
        return '"' + self.value + '"'

    def __attributes(self, checked: bool) -> str:
        """returns the attributes as a string for the config html"""
        string = ""
        if self.__input_attributes:
            string = self.__input_attributes.html()
        if checked:
            string += " checked"
        return string

    @property
    def value(self):
        """Returns Value"""
        return self.__value

    @property
    def label(self):
        """Returns Label"""
        return self.__label

    @property
    def hide_on_html(self):
        """Returns Hide ON HTML"""
        return self.__hide_on_html

    @property
    def not_in_config(self):
        """Returns not in Config"""
        return self.__not_in_config

    @property
    def input_attributes(self) -> Optional[InputAttributes]:
        """returns the input attributes"""
        return self.__input_attributes

    def html_dict(self) -> dict:
        """returns the required Data for the html template to use"""
        return_dict = {
            "label": self.__label,
            "value": self.__value,
        }

        if isinstance(self.input_attributes, InputAttributes):
            return_dict["input_attributes"] = self.input_attributes.html()
        return return_dict
