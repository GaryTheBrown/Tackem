"""Config Object Options Checkbox"""
from typing import Any
from typing import List
from typing import Optional
from typing import Union

from config.backend.obj.data.checkbox import ConfigObjCheckbox
from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.obj.options.base import ConfigObjOptionsBase
from config.backend.rules import ConfigRules


class ConfigObjOptionsCheckBox(ConfigObjOptionsBase):
    """Config Item Options CheckBox"""

    _html_type = "checkbox"

    def __init__(
        self,
        var_name: str,
        values: List[ConfigObjCheckbox],
        default_value: Union[str, int, List[str], List[int]],
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
            if all(not isinstance(x, (str, int)) for x in default_value):
                raise ValueError("default values list is not full of strings or ints")
        if all(not isinstance(x, ConfigObjCheckbox) for x in values):
            raise ValueError("value is not a ConfigObjCheckbox")

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

    @property
    def spec(self) -> str:
        """Returns the line for the config option"""
        if self.not_in_config:
            return ""

        default = self.default_value
        if isinstance(default, list):
            default = "list(" + ", ".join([f"'{x}'" for x in self.default_value]) + ")"
        else:
            default = f"'{self.default_value}'"
        string = f"{self.var_name} = string_list(default={default})\n"

        return string

    def _set_value(self, value: Any):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if len(self.values) != len(value):
            return ConfigObjOptionsBase._set_value(self, value)
        return [v.value for index, v in enumerate(self.values) if value[index] == "1"]
