'''Config Object Float Range'''
from typing import Optional
from libs.config.obj.float_number import ConfigObjFloatNumber
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.button import Button
from libs.config.rules import ConfigRules


class ConfigObjFloatRange(ConfigObjFloatNumber):
    '''Config Item Float Range'''


    __html_type = "range"


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
            button: Optional[Button] = None
    ):
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
            button
        )