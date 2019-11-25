'''Config Object String'''
from typing import Optional
from libs.config.obj.base import ConfigObjBase
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.data_list import DataList
from libs.config.rules import ConfigRules

from libs.html_system import HTMLSystem


class ConfigObjString(ConfigObjBase):
    '''Config Item String'''


    __config_type = "string"
    __html_type = "text"


    def __init__(
            self,
            var_name: str,
            default_value: str,
            label: str,
            priority: int,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            rules: Optional[ConfigRules] = None,
            input_attributes: Optional[InputAttributes] = None,
            data_list: Optional[DataList] = None
    ):
        if not isinstance(default_value, str):
            raise ValueError("Default Value is not a String")

        super().__init__(
            var_name,
            default_value,
            label,
            priority,
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

        string = self.var_name + " = " + self.__config_type + "("
        if self.input_attributes:
            string += self.input_attributes.config_spec
        if self.default_value is not None:
            string += "default="
            string += '"' + self.default_value + '"'
        string += ")\n"

        return string


    @property
    def config_html(self) -> str:
        '''Returns the html for the config option'''
        if self.hide_on_html:
            return ""
        return HTMLSystem.part(
            "inputs/input",
            INPUTTYPE=self.__html_type,
            VARIABLENAME=self.var_name,
            VALUE=self.value,
            OTHER=self.input_attributes.html,
            BUTTON=""#button if button else ""
        )
