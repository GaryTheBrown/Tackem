"""Config Object Boolean"""
from typing import Any
from typing import Optional

from libs.config.obj.base import ConfigObjBase
from libs.config.obj.data.data_list import DataList
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.rules import ConfigRules


DEFAULT_STYLE = {"data_onstyle": "primary", "data_offstyle": "info"}


class ConfigObjBoolean(ConfigObjBase):
    """Config Item Boolean"""

    def __init__(
        self,
        var_name: str,
        default_value: bool,
        label: str,
        help_text: str,
        hide_on_html: bool = False,
        not_in_config: bool = False,
        rules: Optional[ConfigRules] = None,
        input_attributes: Optional[InputAttributes] = None,
        data_list: Optional[DataList] = None,
        value_link: Optional[list] = None,
    ):
        if not isinstance(default_value, bool):
            raise ValueError("default value is not a boolean")
        if input_attributes is None:
            input_attributes = InputAttributes(**DEFAULT_STYLE)
        else:
            input_attributes.add_if_missing(**DEFAULT_STYLE)

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
            value_link,
        )

    def _set_value(self, value):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            if value.lower() in ["true", "on", "yes", "1"]:
                return True
            if value.lower() in ["false", "off", "no", "0"]:
                return False

        if isinstance(value, int):
            if value == 0:
                return False
            return True

        return self.default_value

    @property
    def spec(self) -> str:
        """Returns the line for the config option"""
        if self.not_in_config:
            return ""

        string = self.var_name + " = boolean("

        if self.input_attributes:
            i_a = self.input_attributes.spec
            string += i_a
            if i_a != "":
                string += ", "
        string += f"default='{'True' if self.default_value else 'False'}')\n"
        return string

    def to_type(self, value: Any) -> bool:
        """returns the value in the correct format"""
        try:
            return bool(value)
        except ValueError:
            return False

    def html_dict(self, variable_name: str) -> dict:
        """returns the required Data for the html template to use"""
        return_dict = {"type": "singlecheckbox"}
        return_dict.update(ConfigObjBase.html_dict(self, variable_name))
        return return_dict
