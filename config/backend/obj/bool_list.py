"""Config Object Bool List"""
from typing import Optional

from config.backend.obj.data.data_list import DataList
from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.obj.list import ConfigObjList
from config.backend.rules import ConfigRules


class ConfigObjBoolList(ConfigObjList):
    """Config Item Bool List"""

    _config_type = "bool_list"
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
            if not isinstance(value, bool):
                raise ValueError("Default Value Item is not a bool")

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
