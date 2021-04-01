"""Config Object String List"""
from typing import Optional

from libs.config.obj.data.data_list import DataList
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.list import ConfigObjList
from libs.config.rules import ConfigRules


class ConfigObjStringList(ConfigObjList):
    """Config Item String List"""

    _config_type = "string_list"
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
            if not isinstance(value, str):
                raise ValueError("Default Value Item is not a String")

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

    def html_dict(self, variable_name: str) -> dict:
        """returns the required Data for the html template to use"""
        return_dict = ConfigObjList.html_dict(self, variable_name)

        if return_dict["value"] and isinstance(return_dict["value"], list):
            return_dict["value"] = ", ".join(return_dict["value"])

        if return_dict["default_value"] and isinstance(return_dict["default_value"], list):
            return_dict["default_value"] = ", ".join(return_dict["default_value"])

        return return_dict
