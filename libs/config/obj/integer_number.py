"""Config Object Integer Number"""
from typing import Any
from typing import Optional

from libs.config.obj.base import ConfigObjBase
from libs.config.obj.data.button import Button
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.rules import ConfigRules


class ConfigObjIntegerNumber(ConfigObjBase):
    """Config Item Integer Number"""

    _html_type = "number"

    def __init__(
        self,
        var_name: str,
        default_value: int,
        label: str,
        help_text: str,
        hide_on_html: bool = False,
        not_in_config: bool = False,
        rules: Optional[ConfigRules] = None,
        input_attributes: Optional[InputAttributes] = None,
        button: Optional[Button] = None,
        value_link: Optional[list] = None,
    ):
        if not isinstance(default_value, int):
            raise ValueError("default value is not an int")
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
            value_link,
        )

        self._button = button

    def _set_value(self, value):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if isinstance(value, int):
            return value

        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return self.default_value

        if isinstance(value, float):
            return int(value)

        return self.default_value

    @property
    def spec(self) -> str:
        """Returns the line for the config option"""
        if self.not_in_config:
            return ""

        string = f"{self.var_name} = integer("
        if self.input_attributes:
            i_a = self.input_attributes.spec
            string += i_a
            if i_a != "":
                string += ", "
        string += f"default='{str(self.default_value)}')\n"

        return string

    def to_type(self, value: Any) -> int:
        """returns the value in the correct format"""
        try:
            return int(value)
        except ValueError:
            return 0

    def html_dict(self, variable_name: str) -> dict:
        """returns the required Data for the html template to use"""
        return_dict = {
            "type": "input",
            "input_type": self._html_type,
        }
        return_dict.update(ConfigObjBase.html_dict(self, variable_name))

        if self._button and isinstance(self._button, Button):
            return_dict["button"] = self._button.html_dict()

        return return_dict
