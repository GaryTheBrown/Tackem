'''CONFIG Base Data Class'''
from typing import Any, Optional
from libs.config.rules import ConfigRules


class ConfigBase:
    '''CONFIG Base Class'''

    def __init__(
        self,
        var_name: str,
        label: str,
        help_text: str,
        hide_on_html: bool = False,
        not_in_config: bool = False,
        rules: Optional[ConfigRules] = None,
        value_link: Optional[list] = None
    ):
        if not isinstance(var_name, str):
            raise ValueError("variable name is not a string")
        if not isinstance(label, str):
            raise ValueError("label is not a string")
        if not isinstance(help_text, str):
            raise ValueError("help text is not a string")
        if not isinstance(hide_on_html, bool):
            raise ValueError("hide On HTML is not a bool")
        if not isinstance(not_in_config, bool):
            raise ValueError("not in config is not a bool")
        if rules and not isinstance(rules, ConfigRules):
            raise ValueError("rules is not a config rules object")
        if value_link and not isinstance(value_link, (list, dict)):
            raise ValueError("value link is not a list or dict")

        self.__objects = []
        self.__var_name = var_name
        self.__label = label
        self.__help_text = help_text
        self.__hide_on_html = hide_on_html
        self.__not_in_config = not_in_config
        self.__rules = rules
        self.__value_link = value_link

    @property
    def var_name(self) -> str:
        '''returns the name'''
        return self.__var_name

    @var_name.setter
    def var_name(self, var: Any):
        '''sets the var name'''
        self.__var_name = var

    @property
    def key(self) -> str:
        '''returns the name'''
        return self.__var_name.lower()

    @property
    def label(self):
        '''returns the label'''
        return self.__label

    @label.setter
    def label(self, var: Any):
        '''sets the label'''
        self.__label = var

    @property
    def help_text(self):
        '''returns the help text'''
        return self.__help_text

    @property
    def hide_on_html(self):
        '''returns the hide on html'''
        return self.__hide_on_html

    @property
    def not_in_config(self):
        '''returns the not in config'''
        return self.__not_in_config

    @property
    def rules(self):
        '''returns the rules'''
        return self.__rules

    @property
    def value_link(self):
        '''return the value_link'''
        return self.__value_link
