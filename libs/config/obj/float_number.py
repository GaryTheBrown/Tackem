'''Config Object Float Number'''
from typing import Optional
from libs.config.obj.base import ConfigObjBase
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.button import Button
from libs.config.rules import ConfigRules
from libs.html_system import HTMLSystem


class ConfigObjFloatNumber(ConfigObjBase):
    '''Config Item Float Number'''

    __html_type = "number"

    def __init__(
            self,
            var_name: str,
            default_value: float,
            label: str,
            help_text: str,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            rules: Optional[ConfigRules] = None,
            input_attributes: Optional[InputAttributes] = None,
            button: Optional[Button] = None,
            value_link: Optional[list] = None
    ):
        if not isinstance(default_value, float):
            raise ValueError("default value is not a float")
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
            value_link
        )

        self.__button = button

    def _set_value(self, value) -> Optional[float]:
        '''hidden abstract method for setting the value with checking of type in sub classes'''
        if isinstance(value, float):
            return value

        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                return self.default_value

        if isinstance(value, int):
            return float(value)

        return self.default_value

    @property
    def spec(self) -> str:
        '''Returns the line for the config option'''
        if self.not_in_config:
            return ""

        string = self.var_name + " = float("
        if self.input_attributes:
            i_a = self.input_attributes.spec
            string += i_a
            if i_a != "":
                string += ", "
        string += "default='" + str(self.default_value) + "'"
        string += ")\n"

        return string

    def item_html(self, variable_name: str) -> str:
        '''Returns the html for the config option'''
        if self.hide_on_html:
            return ""
        other = ""
        if isinstance(self.input_attributes, InputAttributes):
            other = self.input_attributes.html()
        button = ""
        if button and not isinstance(button, Button):
            button = self.__button.html
        return HTMLSystem.part(
            "inputs/input",
            INPUTTYPE=self.__html_type,
            VARIABLENAME=variable_name,
            VALUE=self.value,
            OTHER=other,
            BUTTON=button
        )

    def to_type(self, value) -> float:
        '''returns the value in the correct format'''
        try:
            return float(value)
        except ValueError:
            return 0.0
