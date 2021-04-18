"""Config Object Options Checkbox"""
import re
from typing import Any
from typing import Optional

from config.backend.obj.base import ConfigObjBase
from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.rules import ConfigRules


class ConfigObjOptionsBase(ConfigObjBase):
    """Config Item Options CheckBox"""

    def __init__(
        self,
        var_name: str,
        values: list,
        default_value,
        label: str,
        help_text: str,
        hide_on_html: bool = False,
        not_in_config: bool = False,
        rules: Optional[ConfigRules] = None,
        input_attributes: Optional[InputAttributes] = None,
        value_link: Optional[list] = None,
    ):
        super().__init__(
            var_name,
            default_value,
            label,
            help_text,
            hide_on_html,
            not_in_config,
            rules,
            input_attributes,
            value_link,
        )
        self.__values = values

    @property
    def values(self):
        """returns the values"""
        return self.__values

    def _set_value(self, value: Any):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if self.input_attributes and self.input_attributes.multiple:
            return self.__set_value_multi(value)

        if isinstance(value, (int, float)):
            return value

        if isinstance(value, str):
            if isinstance(self.default_value, int):
                try:
                    return int(value)
                except ValueError:
                    return self.default_value
            if isinstance(self.default_value, float):
                try:
                    return float(value)
                except ValueError:
                    return self.default_value
            return str(value)

        if isinstance(value, list):
            return value

        return self.default_value

    def __set_value_multi(self, value: Any):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if isinstance(self.default_value, str):
            return self.__set_value_multi_str(value)

        if isinstance(self.default_value, int):
            return self.__set_value_multi_int(value)

        if isinstance(self.default_value, float):
            return self.__set_value_multi_float(value)

        if isinstance(self.default_value, list):
            return self.__set_value_multi_list(value)

        return self.default_value

    def __set_value_multi_str(self, value: Any):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if isinstance(value, (str, int, float)):
            return str(value)

        if isinstance(value, list):
            return [str(x) for x in value]

        return self.default_value

    def __set_value_multi_int(self, value: Any):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return self.default_value

        if isinstance(value, int):
            return value

        if isinstance(value, float):
            return int(round(value))

        if isinstance(value, list):
            try:
                return [int(x) for x in value]
            except ValueError:
                return self.default_value

        return self.default_value

    def __set_value_multi_float(self, value: Any):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                return self.default_value

        if isinstance(value, int):
            return float(value)

        if isinstance(value, float):
            return value

        if isinstance(value, list):
            try:
                return [float(x) for x in value]
            except ValueError:
                return self.default_value

        return self.default_value

    def __set_value_multi_list(self, value: Any):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if isinstance(value, str):
            self.__set_value_multi_list_str(value)

        if isinstance(value, int):
            self.__set_value_multi_list_int(value)

        if isinstance(value, float):
            self.__set_value_multi_list_float(value)

        if isinstance(value, list):
            self.__set_value_multi_list_list(value)
        return self.default_value

    def __set_value_multi_list_str(self, value: Any):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if ";" in value or "," in value or "\n" in value:
            return self.__set_value_multi_list_list(
                [str(x).strip() for x in re.split(";|,|\n", value)]
            )

        if isinstance(self.default_value[0], str):
            return str(value)

        if isinstance(self.default_value[0], int):
            try:
                return int(value)
            except ValueError:
                return self.default_value

        if isinstance(self.default_value[0], float):
            try:
                return float(value)
            except ValueError:
                return self.default_value

        return self.default_value

    def __set_value_multi_list_int(self, value: Any):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if isinstance(self.default_value[0], str):
            return str(value)

        if isinstance(self.default_value[0], int):
            return value

        if isinstance(self.default_value[0], float):
            try:
                return float(value)
            except ValueError:
                return self.default_value

        return self.default_value

    def __set_value_multi_list_float(self, value: Any):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if isinstance(self.default_value[0], str):
            return str(value)

        if isinstance(self.default_value[0], int):
            try:
                return int(value)
            except ValueError:
                return self.default_value

        if isinstance(self.default_value[0], float):
            return float(value)

        return self.default_value

    def __set_value_multi_list_list(self, value: Any):
        """hidden abstract method for setting the value with checking of type in sub classes"""
        if isinstance(self.default_value[0], str):
            return [str(x) for x in value]

        if isinstance(self.default_value[0], int):
            try:
                return [int(x) for x in value]
            except ValueError:
                return self.default_value

        if isinstance(self.default_value[0], float):
            try:
                return [float(x) for x in value]
            except ValueError:
                return self.default_value

        return self.default_value

    @property
    def spec(self) -> str:
        """Returns the line for the config option"""
        if self.not_in_config:
            return ""

        string = self.var_name + " = option("
        string += ", ".join([value.spec for value in self.__values])
        string += ", default='" + self.default_value + "'"
        string += ")\n"

        return string

    def html_dict(self, variable_name: str) -> dict:
        """returns the required Data for the html template to use"""
        return_dict = {
            "type": self._html_type,
            "values": [o.html_dict() for o in self.__values if not o.hide_on_html],
        }
        return_dict.update(ConfigObjBase.html_dict(self, variable_name))
        return return_dict
