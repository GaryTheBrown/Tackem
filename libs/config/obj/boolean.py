'''Config Object Boolean'''
from typing import Optional
from libs.config.obj.base import ConfigObjBase
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.data_list import DataList
from libs.config.rules import ConfigRules
from libs.html_system import HTMLSystem

class ConfigObjBoolean(ConfigObjBase):
    '''Config Item Boolean'''

    def __init__(
            self,
            var_name: str,
            default_value: bool,
            label: str,
            help_text: str,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            rules: Optional[ConfigRules] = None,
            input_attributes: Optional[InputAttributes] = None,
            data_list: Optional[DataList] = None,
            value_link: Optional[list] = None
    ):
        if not isinstance(default_value, bool):
            raise ValueError("default value is not a boolean")

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
            value_link
        )

    def _set_value(self, value) -> bool:
        '''hidden abstract method for setting the value with checking of type in sub classes'''
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            if value.lower() in ["true", "on", "yes", "1"]:
                return True
            if value.lower() in ["false", "off", "no", "0"]:
                return False

        if isinstance(value, int):
            if value == 0:
                return False
            return True

        return self.default_value

    @property
    def spec(self) -> str:
        '''Returns the line for the config option'''
        if self.not_in_config:
            return ""

        string = self.var_name + " = boolean("

        if self.input_attributes:
            i_a = self.input_attributes.spec
            string += i_a
            if i_a != "":
                string += ", "
        string += "default='" + \
            ("True" if self.default_value else "False") + "'"
        string += ")\n"

        return string

    def item_html(self, variable_name: str) -> str:
        '''Returns the html for the config option'''
        if self.hide_on_html:
            return ""
        other = ""
        if isinstance(self.input_attributes, InputAttributes):
            other = self.input_attributes.html()
        return HTMLSystem.part(
            "inputs/singlecheckbox",
            VARIABLENAME=variable_name,
            VALUE=self.value,
            CHECKED="checked" if self.value else "",
            ENABLED=str(self.value),
            OTHER=other
        )

    def to_type(self, value) -> bool:
        '''returns the value in the correct format'''
        try:
            return bool(value)
        except ValueError:
            return False
