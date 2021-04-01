"""Config Object List"""
from typing import Optional

from libs.config.obj.base import ConfigObjBase
from libs.config.obj.data.data_list import DataList
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.rules import ConfigRules


class ConfigObjList(ConfigObjBase):
    """Config Item List"""

    _config_type = "list"
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

    def _set_value(self, value):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return value.replace(" ", "").split(",")
        return self.default_value

    @property
    def spec(self) -> str:
        """Returns the line for the config option"""
        if self.not_in_config:
            return ""

        string = f"{self.var_name} = {self._config_type}("
        if self.input_attributes:
            i_a = self.input_attributes.spec
            string += i_a
            if i_a != "":
                string += ", "

        string += f"default=list({self._default_list_to_spec}))\n"

        return string

    @property
    def _default_list_to_spec(self) -> str:
        """Created the default value String"""
        return_list = []
        for value in self.default_value:
            if isinstance(value, str):
                return_list.append(f"'{value}'")
            elif isinstance(value, (int, float)):
                return_list.append(value)
        return ", ".join(return_list)

    def html_dict(self, variable_name: str) -> dict:
        """returns the required Data for the html template to use"""
        return_dict = {
            "type": "input",
            "input_type": self._html_type,
        }
        return_dict.update(ConfigObjBase.html_dict(self, variable_name))

        return return_dict
