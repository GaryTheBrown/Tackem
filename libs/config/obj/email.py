'''Config Obj String'''
from typing import Optional
from libs.config.obj.base import ConfigObjBase
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.rules import ConfigRules
from libs.html_system import HTMLSystem


class ConfigObjString(ConfigObjBase):
    '''Config Obj String'''

    def __init__(
            self,
            var_name: str,
            default_value: str,
            label: str,
            priority: int,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            input_attributes: Optional[InputAttributes] = None,
            rules: Optional[ConfigRules] = None,
            data_set: Optional[list] = None # List Of Options
    ):
        if not isinstance(default_value, str):
            raise ValueError("Default Value is not a String")
        super().__init__(
            var_name,
            default_value,
            label,
            priority,
            hide_on_html,
            not_in_config,
            input_attributes,
            rules
        )

        self.__data_set = data_set


    def config_spec(self) -> str:
        '''Returns the line for the config option'''
        if self.not_in_config:
            return ""
        return_string = self.var_name + " = " + "email("

        if self.default_value is not None:
            return_string += "default="
            return_string += '"' + self.default_value + '"'
        return_string += ")\n"
        return return_string


    def config_html(self) -> str:
        '''Returns the html for the config option'''
        return HTMLSystem.part(
            "inputs/input",
            INPUTTYPE="email",
            VARIABLENAME=self.var_name,
            VALUE=self.value,
            OTHER=self.input_attributes.html(),
            BUTTON=""#button if button else ""
        )

    @property
    def data_set(self) -> Optional[list]:
        '''returns the data set'''
        return self.__data_set
