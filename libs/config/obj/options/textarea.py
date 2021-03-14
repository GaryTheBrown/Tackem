'''Config Object Options Radio'''
from typing import Optional, List, Union
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.radio import ConfigObjRadio
from libs.config.obj.options.base import ConfigObjOptionsBase
from libs.config.rules import ConfigRules
from libs.html_system import HTMLSystem


class ConfigObjOptionsTextArea(ConfigObjOptionsBase):
    '''Config Item Options Radio'''

    def __init__(
            self,
            var_name: str,
            values: List[ConfigObjRadio],
            default_value: Union[str, int],
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
        if not isinstance(default_value, (str, list)):
            raise ValueError("default value is not a list or str")
        if all(not isinstance(x, ConfigObjRadio) for x in values):
            raise ValueError("value is not a ConfigObjRadio")
        if input_attributes:
            input_attributes.block("multiple")

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
        return HTMLSystem.part(
            "inputs/textarea",
            VARIABLENAME=self.var_name,
            VALUE=self.value,
            OTHER=self.input_attributes.html,
            ROWS=5
        )
