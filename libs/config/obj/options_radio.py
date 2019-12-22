'''Config Object Options Radio'''
from typing import Optional, List
from libs.config.obj.base import ConfigObjBase
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.radio import ConfigObjRadio
from libs.config.rules import ConfigRules


class ConfigObjOptionsRadio(ConfigObjBase):
    '''Config Item Options Radio'''


    def __init__(
            self,
            var_name: str,
            values: List[ConfigObjRadio],
            default_value: int,
            label: str,
            help_text: str,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            rules: Optional[ConfigRules] = None,
            input_attributes: Optional[InputAttributes] = None,
    ):
        if not isinstance(values, list):
            raise ValueError("values is not a value")
        if not isinstance(default_value, int):
            raise ValueError("default value is not a int")
        for value in values:
            if not isinstance(value, ConfigObjRadio):
                raise ValueError("value is not a ConfigObjRadio")
        if input_attributes:
            input_attributes.block("multiple")

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
            options += value.html(count == self.value)
        return options


    @property
    def values(self) -> list:
        '''returns the values in a list'''
        return self.__values
