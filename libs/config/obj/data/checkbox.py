'''Config Object Checkbox'''
from libs.html_system import HTMLSystem


class ConfigObjCheckbox:
    '''Config Item Checkbox'''


    def __init__(
            self,
            value: str,
            label: str,
            disabled: bool = False,
            read_only: bool = False,
            checked: bool = False,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            short_label: str = ""
    ):
        if not isinstance(value, str):
            raise ValueError("value is not a string")
        if not isinstance(label, str):
            raise ValueError("label is not a string")
        if not isinstance(disabled, bool):
            raise ValueError("disabled is not a bool")
        if not isinstance(read_only, bool):
            raise ValueError("read only is not a bool")
        if not isinstance(checked, bool):
            raise ValueError("checked is not a bool")
        if not isinstance(hide_on_html, bool):
            raise ValueError("hide On HTML is not a bool")
        if not isinstance(not_in_config, bool):
            raise ValueError("not in config is not a bool")
        if not isinstance(short_label, str):
            raise ValueError("short label not a string")

        self.__value = value
        self.__label = label
        self.__disabled = disabled
        self.__checked = checked
        self.__hide_on_html = hide_on_html
        self.__not_in_config = not_in_config
        self.__short_label = short_label


    @property
    def config_spec(self) -> str:
        '''Returns the line for the config option'''
        if self.not_in_config:
            return ""
        return '"' + self.value + '"'


    @property
    def __attributes(self) -> str:
        '''returns the attributes as a string for the config html'''
        string = ""
        if self.__disabled:
            string += "disabled"
        if self.__checked:
            string += " checked"
        if self.__short_label != "":
            string += ' label="' + self.__short_label + '"'
        return string


    @property
    def html(self) -> str:
        '''Returns the option html for the config'''
        if self.__hide_on_html:
            return ""
        return HTMLSystem.part(
            "inputs/single/checkbox",
            VALUE=self.__value,
            LABEL=self.__label,
            OTHER=self.__attributes
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
    def disabled(self):
        '''Returns Disabled'''
        return self.__disabled


    @property
    def checked(self):
        '''Returns Selected'''
        return self.__checked


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
