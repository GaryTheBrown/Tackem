'''Config Object Options Radio'''
from typing import Optional, List, Union
from libs.config.obj.options_base import ConfigObjOptionsBase
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.radio import ConfigObjRadio
from libs.config.rules import ConfigRules


class ConfigObjOptionsRadio(ConfigObjOptionsBase):
    '''Config Item Options Radio'''


    def __init__(
            self,
            var_name: str,
            values: List[ConfigObjRadio],
            default_value: Union[str, int],
            label: str,
            help_text: str,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            rules: Optional[ConfigRules] = None,
            input_attributes: Optional[InputAttributes] = None,
    ):
        if not isinstance(values, list):
            raise ValueError("values is not a value")
        if not isinstance(default_value, (str, int)):
            raise ValueError("default value is not a int or str")
        if all(not isinstance(x, ConfigObjRadio) for x in values):
            raise ValueError("value is not a ConfigObjRadio")
        if input_attributes:
            input_attributes.block("multiple")

        super().__init__(
            var_name,
            values,
            default_value,
            label,
            help_text,
            hide_on_html,
            not_in_config,
            rules,
            input_attributes
        )


    def item_html(self, variable_name: str, value,) -> str:
        '''Returns the html for the config option'''
        if self.hide_on_html:
            return ""
        options = ""
        for count, value in enumerate(self.__values):
            options += value.html(count == self.value)
        return options


    def default_set(self, default_value, value_list=None) ->  Union[int, List[int]]:
        '''sorts out the default value'''

        if isinstance(default_value, int):
            return default_value

        if value_list is None:
            value_list = self.__values

        if isinstance(default_value, str):
            for i, item in enumerate(value_list):
                if item.value == default_value:
                    return i
        return -1
