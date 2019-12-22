'''Config Object Options Select'''
from typing import Optional, List, Union
from libs.config.obj.base import ConfigObjBase
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.option import ConfigObjOption
from libs.config.rules import ConfigRules
from libs.html_system import HTMLSystem


class ConfigObjOptionsSelect(ConfigObjBase):
    '''Config Item Options Select'''


    def __init__(
            self,
            var_name: str,
            values: List[ConfigObjOption],
            default_value: Union[int, List[int]],
            label: str,
            help_text: str,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            rules: Optional[ConfigRules] = None,
            input_attributes: Optional[InputAttributes] = None,
    ):
        if not isinstance(values, list):
            raise ValueError("values is not a value")
        if not isinstance(default_value, int) and not isinstance(default_value, list):
            raise ValueError("default value is not a int or list of ints")
        for value in values:
            if not isinstance(value, ConfigObjOption):
                raise ValueError("value is not a ConfigObjOption")

        super().__init__(
            var_name,
            default_value,
            label,
            help_text,
            hide_on_html,
            not_in_config,
            rules,
            input_attributes
        )
        self.__values = values


    @property
    def config_spec(self) -> str:
        '''Returns the line for the config option'''
        if self.not_in_config:
            return ""

        string = self.var_name + " = options("
        string += ", ".join([value.config_spec for value in self.__values])
        string += ")\n"

        return string


    @property
    def config_html(self) -> str:
        '''Returns the html for the config option'''
        if self.hide_on_html:
            return ""
        options = ""
        for count, value in enumerate(self.__values):
            options += value.html((isinstance(self.value, int) and count == self.value) \
                               or (isinstance(self.value, list) and count in self.value))
        other = ""
        if isinstance(self.input_attributes, InputAttributes):
            other = self.input_attributes.html

        return HTMLSystem.part(
            "inputs/select",
            OPTIONS=options,
            VARIABLENAME=self.var_name,
            OTHER=other
        )


    @property
    def values(self) -> list:
        '''returns the values in a list'''
        return self.__values
