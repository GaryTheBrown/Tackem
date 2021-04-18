"""Config Item Password"""
from typing import Optional

from config.backend.obj.data.button import Button
from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.obj.string import ConfigObjString
from config.backend.rules import ConfigRules


class ConfigObjPassword(ConfigObjString):
    """Config Item Password"""

    _config_type = "string"
    _html_type = "password"

    def __init__(
        self,
        var_name: str,
        label: str,
        help_text: str,
        hide_on_html: bool = False,
        not_in_config: bool = False,
        rules: Optional[ConfigRules] = None,
        input_attributes: Optional[InputAttributes] = None,
        button: Optional[Button] = None,
        value_link: Optional[list] = None,
    ):
        super().__init__(
            var_name,
            "",
            label,
            help_text,
            hide_on_html,
            not_in_config,
            rules,
            input_attributes,
            button,
            value_link,
        )
