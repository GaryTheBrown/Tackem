"""Config Object Options Radio"""
from typing import List
from typing import Optional
from typing import Union

from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.obj.data.radio import ConfigObjRadio
from config.backend.obj.options.base import ConfigObjOptionsBase
from config.backend.rules import ConfigRules


class ConfigObjOptionsRadio(ConfigObjOptionsBase):
    """Config Item Options Radio"""

    _html_type = "radio"

    def __init__(
        self,
        var_name: str,
        values: List[ConfigObjRadio],
        default_value: Union[str, int],
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
        if not isinstance(default_value, (str, int)):
            raise ValueError("default value is not a int or str")
        if all(not isinstance(x, ConfigObjRadio) for x in values):
            raise ValueError("value is not a ConfigObjRadio")
        if input_attributes:
            input_attributes.block("multiple")

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
