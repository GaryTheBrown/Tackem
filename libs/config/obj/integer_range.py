'''Config Object Integer Range'''
from typing import Optional
from libs.config.obj.integer_number import ConfigObjIntegerNumber
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.rules import ConfigRules


class ConfigObjIntegerRange(ConfigObjIntegerNumber):
    '''Config Item Integer Range'''


    __html_type = "range"


    def __init__(
            self,
            var_name: str,
            default_value: int,
            label: str,
            priority: int,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            rules: Optional[ConfigRules] = None,
            input_attributes: Optional[InputAttributes] = None
    ):
        input_attributes.needed("min", "max", "step")

        super().__init__(
            var_name,
            default_value,
            label,
            priority,
            hide_on_html,
            not_in_config,
            rules,
            input_attributes
        )
