'''Config Object Options Checkbox'''
from typing import Optional, List, Union
from libs.config.obj.base import ConfigObjBase
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.rules import ConfigRules


class ConfigObjOptionsBase(ConfigObjBase):
    '''Config Item Options CheckBox'''


    def __init__(
            self,
            var_name: str,
            values: list,
            default_value: Union[str, int, List[str], List[int]],
            label: str,
            help_text: str,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            rules: Optional[ConfigRules] = None,
            input_attributes: Optional[InputAttributes] = None,
    ):
        super().__init__(
            var_name,
            self.default_set(default_value, values),
            label,
            help_text,
            hide_on_html,
            not_in_config,
            rules,
            input_attributes
        )
        self.__values = values


    @property
    def spec(self) -> str:
        '''Returns the line for the config option'''
        if self.not_in_config:
            return ""

        string = self.var_name + " = option("
        string += ", ".join([value.spec for value in self.__values])
        string += ", default='" + self.__values[self.default_value].value + "'"
        string += ")\n"

        return string


    def item_html(self, variable_name: str, value) -> str:
        '''Returns the html for the config option'''
        if self.hide_on_html:
            return ""
        data = ""
        for count, value in enumerate(self.__values):
            data += value.html(
                (isinstance(self.default_value, int) and count == self.default_value) \
                or (isinstance(self.default_value, list) and count in self.default_value)
            )
        return data


    @property
    def values(self) -> list:
        '''returns the values in a list'''
        return self.__values


    def to_type(self, value) -> list:
        '''returns the value in the correct format'''
        if isinstance(value, list):
            return value
        return []


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

        if isinstance(default_value, list):
            if all(not isinstance(x, int) for x in default_value):
                return default_value
            fixed_list = []
            for value in default_value:
                if isinstance(value, int):
                    fixed_list.append(value)
                elif isinstance(value, str):
                    for i, list_value in enumerate(value_list):
                        if value == list_value.value:
                            fixed_list.append(i)
                            break
            return fixed_list
        return -1
