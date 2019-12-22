'''Config Obj String'''
from typing import Optional
from libs.config.obj.string import ConfigObjString
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.button import Button
from libs.config.rules import ConfigRules


class ConfigObjEmail(ConfigObjString):
    '''Config Obj String'''


    __config_type = "email"
    __html_type = "email"


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
            button: Optional[Button] = None
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
            button
        )
