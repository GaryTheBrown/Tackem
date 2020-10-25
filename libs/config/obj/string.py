'''Config Object String'''
from typing import Any, Optional
from libs.config.obj.base import ConfigObjBase
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.data_list import DataList
from libs.config.obj.data.button import Button
from libs.config.rules import ConfigRules
from libs.html_system import HTMLSystem

class ConfigObjString(ConfigObjBase):
    '''Config Item String'''

    __config_type = "string"
    __html_type = "text"

    def __init__(
            self,
            var_name: str,
            default_value: str,
            label: str,
            help_text: str,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            rules: Optional[ConfigRules] = None,
            input_attributes: Optional[InputAttributes] = None,
            data_list: Optional[DataList] = None,
            button: Optional[Button] = None,
            value_link: Optional[list] = None
    ):
        if not isinstance(default_value, str):
            raise ValueError("Default Value is not a String")
        if button and not isinstance(button, Button):
            raise ValueError("Button is not a Button Obj")

        super().__init__(
            var_name,
            default_value,
            label,
            help_text,
            hide_on_html,
            not_in_config,
            rules,
            input_attributes,
            data_list,
            value_link
        )
        self.__button = button

    def _set_value(self, value: Any):
        '''hidden abstract method for setting the value with checking of type in sub classes'''
        return str(value)

    @property
    def spec(self) -> str:
        '''Returns the line for the config option'''
        if self.not_in_config:
            return ""

        string = f"{self.var_name} = {self.__config_type}("
        if self.input_attributes:
            i_a = self.input_attributes.spec
            string += i_a
            if i_a != "":
                string += ", "
        string += f"default='{str(self.default_value)}')\n"

        return string

    def item_html(self, variable_name: str) -> str:
        '''Returns the html for the config option'''
        if self.hide_on_html:
            return ""
        other = ""
        if isinstance(self.input_attributes, InputAttributes):
            other = self.input_attributes.html()
        button = ""
        if self.__button and isinstance(self.__button, Button):
            button = self.__button.html
        return HTMLSystem.part(
            "inputs/input",
            INPUTTYPE=self.__html_type,
            VARIABLENAME=variable_name,
            VALUE=self.value,
            OTHER=other,
            BUTTON=button
        )

    def to_type(self, value: Any) -> str:
        '''returns the value in the correct format'''
        try:
            return str(value)
        except ValueError:
            return ""
