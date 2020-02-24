'''Config Object Options Select'''
from typing import Optional, List, Union
from libs.config.obj.options.base import ConfigObjOptionsBase
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.option import ConfigObjOption
from libs.config.rules import ConfigRules
from libs.html_system import HTMLSystem


class ConfigObjOptionsSelect(ConfigObjOptionsBase):
    '''Config Item Options Select'''


    def __init__(
            self,
            var_name: str,
            values: List[ConfigObjOption],
            default_value: Union[str, int, float],
            label: str,
            help_text: str,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            rules: Optional[ConfigRules] = None,
            input_attributes: Optional[InputAttributes] = None,
            value_link: Optional[list] = None
    ):
        if not isinstance(values, list):
            raise ValueError("values is not a value")
        if not isinstance(default_value, (str, int, list)):
            raise ValueError("default value is not a string, int or list")
        if isinstance(default_value, list):
            for i, val in enumerate(default_value):
                if not isinstance(val, (str, int, float)):
                    raise ValueError("default value item is not a string, int or float")
        for value in values:
            if not isinstance(value, ConfigObjOption):
                raise ValueError("value is not a ConfigObjOption")

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
            value_link
        )


    def item_html(self, variable_name: str) -> str:
        '''Returns the html for the config option'''
        if self.hide_on_html:
            return ""
        other = ""
        if isinstance(self.input_attributes, InputAttributes):
            other = self.input_attributes.html
        return HTMLSystem.part(
            "inputs/select",
            OPTIONS=super().item_html(variable_name),
            VARIABLENAME=variable_name,
            OTHER=other
        )
