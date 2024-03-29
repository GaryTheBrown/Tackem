"""Config Object Integer Range"""
from typing import Optional

from config.backend.obj.data.button import Button
from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.obj.integer_number import ConfigObjIntegerNumber
from config.backend.rules import ConfigRules


class ConfigObjIntegerRange(ConfigObjIntegerNumber):
    """Config Item Integer Range"""

    _html_type = "range"

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
        if input_attributes and not isinstance(input_attributes, InputAttributes):
            raise ValueError("input_attributes not correct type")
        input_attributes.needed("min", "max", "step")

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
