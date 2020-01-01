'''Config Object Checkbox'''
from typing import Optional
from libs.html_system import HTMLSystem
from libs.config.obj.data.input_attributes import InputAttributes


class ConfigObjCheckbox:
    '''Config Item Checkbox'''


    def __init__(
            self,
            value: str,
            label: str,
            read_only: bool = False,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            short_label: str = "",
            input_attributes: Optional[InputAttributes] = None,
    ):
        if not isinstance(value, str):
            raise ValueError("value is not a string")
        if not isinstance(label, str):
            raise ValueError("label is not a string")
        if not isinstance(read_only, bool):
            raise ValueError("read only is not a bool")
        if not isinstance(hide_on_html, bool):
            raise ValueError("hide On HTML is not a bool")
        if not isinstance(not_in_config, bool):
            raise ValueError("not in config is not a bool")
        if not isinstance(short_label, str):
            raise ValueError("short label not a string")
        if input_attributes:
            if not isinstance(input_attributes, InputAttributes):
                raise ValueError("input_attributes not correct type")
            input_attributes.block("autofocus", "multiple", "required")

        self.__value = value
        self.__label = label
        self.__hide_on_html = hide_on_html
        self.__not_in_config = not_in_config
        self.__short_label = short_label
        self.__input_attributes = input_attributes


    @property
    def spec(self) -> str:
        '''Returns the line for the config option'''
        if self.not_in_config:
            return ""
        return '"' + self.value + '"'


    def __attributes(self, checked) -> str:
        '''returns the attributes as a string for the config html'''
        string = ""
        if self.__input_attributes:
            string = self.__input_attributes.html()
        if checked:
            string += " checked"
        if self.__short_label != "":
            string += ' label="' + self.__short_label + '"'
        return string


    def html(self, checked) -> str:
        '''Returns the option html for the config'''
        if self.__hide_on_html:
            return ""
        return HTMLSystem.part(
            "inputs/single/checkbox",
            VALUE=self.__value,
            LABEL=self.__label,
            OTHER=self.__attributes(checked)
        )


    @property
    def value(self):
        '''Returns Value'''
        return self.__value


    @property
    def label(self):
        '''Returns Label'''
        return self.__label


    @property
    def hide_on_html(self):
        '''Returns Hide ON HTML'''
        return self.__hide_on_html


    @property
    def not_in_config(self):
        '''Returns not in Config'''
        return self.__not_in_config


    @property
    def short_label(self):
        '''Returns the Shortened Label'''
        return self.__short_label


    @property
    def input_attributes(self) -> Optional[InputAttributes]:
        '''returns the input attributes'''
        return self.__input_attributes
