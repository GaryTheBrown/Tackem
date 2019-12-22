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
            data_list: Optional[DataList] = None
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
            data_list
        )


    @property
    def config_spec(self) -> str:
        '''Returns the line for the config option'''
        if self.not_in_config:
            return ""

        string = self.var_name + " = boolean("
        if self.input_attributes:
            string += self.input_attributes.config_spec
        string += ")\n"

        return string


    @property
    def config_html(self) -> str:
        '''Returns the html for the config option'''
        if self.hide_on_html:
            return ""
        other = ""
        if isinstance(self.input_attributes, InputAttributes):
            other = self.input_attributes.html

        return HTMLSystem.part(
            "inputs/singlecheckbox",
            VARIABLENAME=self.var_name,
            VALUE=self.value,
            CHECKED="checked" if self.value else "",
            ENABLED=str(self.value),
            OTHER=other
        )
