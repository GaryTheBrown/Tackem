'''Config Object Options Checkbox'''
from typing import Optional, List, Union
from libs.config.obj.base import ConfigObjBase
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.checkbox import ConfigObjCheckbox
from libs.config.rules import ConfigRules


class ConfigObjOptionsCheckBox(ConfigObjBase):
    '''Config Item Options CheckBox'''


    def __init__(
            self,
            var_name: str,
            values: List[ConfigObjCheckbox],
            default_value: Union[int, List[int]],
            label: str,
            priority: int,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            rules: Optional[ConfigRules] = None,
            input_attributes: Optional[InputAttributes] = None,
    ):
        if not isinstance(values, list):
            raise ValueError("values is not a value")
        for value in values:
            if not isinstance(value, ConfigObjCheckbox):
                raise ValueError("value is not a ConfigObjCheckbox")

        super().__init__(
            var_name,
            default_value,
            label,
            priority,
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
        return "".join([value.html for value in self.__values])


    @property
    def values(self) -> list:
        '''returns the values in a list'''
        return self.__values
