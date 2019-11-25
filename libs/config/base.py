'''Config Base Data Class'''
from typing import Optional
from libs.config.rules import ConfigRules
class ConfigBase:
    '''Config Base Class'''


    def __init__(
            self,
            var_name: str,
            label: str,
            help_text: str,
            priority: int,
            hide_on_html: bool = False,
            not_in_config: bool = False,
            rules: Optional[ConfigRules] = None,
        ):
        if not isinstance(var_name, str):
            raise ValueError("variable name is not a string")
        if not isinstance(label, str):
            raise ValueError("label is not a string")
        if not isinstance(help_text, str):
            raise ValueError("help text is not a string")
        if not isinstance(priority, int):
            raise ValueError("priority is not a int")
        if not isinstance(hide_on_html, bool):
            raise ValueError("hide On HTML is not a bool")
        if not isinstance(not_in_config, bool):
            raise ValueError("not in config is not a bool")
        if rules and not isinstance(rules, ConfigRules):
            raise ValueError("rules is not a config rules object")

        self.__objects = []
        self.__var_name = var_name
        self.__label = label
        self.__help_text = help_text
        self.__priority = priority
        self.__hide_on_html = hide_on_html
        self.__not_in_config = not_in_config
        self.__rules = rules


    @property
    def var_name(self):
        '''returns the name'''
        return self.__var_name


    @property
    def label(self):
        '''returns the label'''
        return self.__label


    @property
    def help_text(self):
        '''returns the help text'''
        return self.__help_text


    @property
    def priority(self):
        '''returns the priority'''
        return self.__priority


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
