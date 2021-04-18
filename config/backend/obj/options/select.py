"""Config Object Options Select"""
from typing import List
from typing import Optional
from typing import Union

from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.obj.data.option import ConfigObjOption
from config.backend.obj.options.base import ConfigObjOptionsBase
from config.backend.rules import ConfigRules


class ConfigObjOptionsSelect(ConfigObjOptionsBase):
    """Config Item Options Select"""

    _html_type = "select"

    def __init__(
        self,
        var_name: str,
        values: List[ConfigObjOption],
        default_value: Union[str, int, float],
        label: str,
        help_text: str,
        hide_on_html: bool = False,
        not_in_config: bool = False,
        rules: Optional[ConfigRules] = None,
        input_attributes: Optional[InputAttributes] = None,
        value_link: Optional[list] = None,
    ):
        if not isinstance(values, list):
            raise ValueError("values is not a value")
        if not isinstance(default_value, (str, int, list)):
            raise ValueError("default value is not a string, int or list")
        if isinstance(default_value, list):
            for val in default_value:
                if not isinstance(val, (str, int, float)):
                    raise ValueError("default value item is not a string, int or float")
        for value in values:
            if not isinstance(value, ConfigObjOption):
                raise ValueError("value is not a ConfigObjOption")

        super().__init__(
            var_name,
            values,
            default_value,
            label,
            help_text,
            hide_on_html,
            not_in_config,
            rules,
            input_attributes,
            value_link,
        )
