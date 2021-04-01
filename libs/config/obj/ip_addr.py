"""Config Object String"""
from typing import Optional

from libs.config.obj.data.button import Button
from libs.config.obj.data.data_list import DataList
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.string import ConfigObjString
from libs.config.rules import ConfigRules


class ConfigObjIpAddr(ConfigObjString):
    """Config Item Ip Address"""

    _config_type = "ip_addr"
    _html_type = "text"

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
        data_list: Optional[DataList] = None,
        button: Optional[Button] = None,
        value_link: Optional[list] = None,
    ):
        if not isinstance(default_value, str):
            raise ValueError("Default Value is not an Ip Address")
        ip_split = default_value.split(".")
        if len(ip_split) != 4:
            raise ValueError("Default Value is not an Ip Address")
        for section in ip_split:
            try:
                _ = int(section)
            except ValueError:
                raise ValueError("Default Value is not an Ip Address")

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
        self._button = button

    def _set_value(self, value):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if not isinstance(value, str):
            return self.default_value

        ip_split = value.split(".")
        if len(ip_split) != 4:
            return self.default_value
        for section in ip_split:
            try:
                _ = int(section)
            except ValueError:
                return self.default_value

        return str(value)
