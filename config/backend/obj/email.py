"""Config Obj String"""
import re
from typing import Optional

from config.backend.obj.data.button import Button
from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.obj.string import ConfigObjString
from config.backend.rules import ConfigRules


class ConfigObjEmail(ConfigObjString):
    """Config Obj String"""

    _config_type = "email"
    _html_type = "email"

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
        button: Optional[Button] = None,
        value_link: Optional[list] = None,
    ):
        if not isinstance(default_value, str):
            raise ValueError("default value is not a string")
        super().__init__(
            var_name,
            default_value,
            label,
            help_text,
            hide_on_html,
            not_in_config,
            rules,
            input_attributes,
            button,
            value_link,
        )

    def _set_value(self, value):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if not isinstance(value, str):
            return self.default_value

        if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", value) is not None:
            return value
        return self.default_value
