'''Config Item Password'''
from typing import Optional
from libs.config.obj.string import ConfigObjString
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.rules import ConfigRules

class ConfigObjPassword(ConfigObjString):
    '''Config Item Password'''

    __config_type = "string"
    __html_type = "password"


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
