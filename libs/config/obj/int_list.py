"""Config Object Int List"""
from typing import Optional

from libs.config.obj.data.data_list import DataList
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.list import ConfigObjList
from libs.config.rules import ConfigRules


class ConfigObjIntList(ConfigObjList):
    """Config Item Int List"""

    _config_type = "int_list"
    _html_type = "text"

    def __init__(
        self,
        var_name: str,
        default_value: list,
        label: str,
        help_text: str,
        hide_on_html: bool = False,
        not_in_config: bool = False,
        rules: Optional[ConfigRules] = None,
        input_attributes: Optional[InputAttributes] = None,
        data_list: Optional[DataList] = None,
        value_link: Optional[list] = None,
    ):
        if not isinstance(default_value, list):
            raise ValueError("Default Value is not a List")

        for value in default_value:
            if not isinstance(value, int):
                raise ValueError("Default Value Item is not a Int")

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
