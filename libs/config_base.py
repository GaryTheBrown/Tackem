'''Base class for config object and config option'''
from typing import Union

class ConfigBase:
    '''Base Functions shared between config_object and config_option'''

    def __init__(
            self,
            name: str,
            label: str,
            priority: int,
            script: Union[str, None],
            hide_from_html: bool,
            read_only: bool,
            disabled: bool,
            show: Union[str, list, None],
            hide: Union[str, list, None],
            toggle_section: Union[str, None],
            toggle_sections: Union[list, None],
            enable_disable,
            section_controller
    ):
        self._name = name
        self._label = label
        self._priority = priority
        self._script = script
        self._hide_on_html = hide_from_html
        self._read_only = read_only
        self._disabled = disabled
        self._show = show
        self._hide = hide
        self._toggle_section = toggle_section
        self._toggle_sections = toggle_sections
        self._enable_disable = enable_disable
        self._section_controller = section_controller


    def label(self):
        '''return label'''
        return self._label


    def read_only(self):
        '''returns read only'''
        return self._read_only


    def disabled(self):
        '''return disabled'''
        return self._disabled


    def priority(self):
        '''return priority'''
        return self._priority


    def section_controller(self):
        '''returns the link to the controller'''
        return self._section_controller


    def show_or_hide(self, key):
        '''returns if the key should be hidden or shown'''
        if self._toggle_sections:
            if key in self._toggle_sections[0]:
                return True
            elif key in self._toggle_sections[1]:
                return False
        elif self._show:
            if self._show == key:
                return True
        elif self._hide:
            if self._hide == key:
                return False
        return None


    def __script_create_check(self):
        '''checks if any scripts are in the option'''
        if self._show:
            return True
        if self._hide:
            return True
        if self._toggle_section:
            return True
        if self._toggle_sections:
            return True
        return False


    def _script_create(self, script_call):
        '''returns the script'''
        if self.__script_create_check():
            return_string = ' '
            return_string += script_call
            return_string += '="'
            if isinstance(self._show, str):
                return_string += self._show_call(self._show)
            elif isinstance(self._show, list):
                for show in self._show:
                    return_string += self._show_call(show)
            if isinstance(self._hide, str):
                return_string += self._hide_call(self._hide)
            elif isinstance(self._hide, list):
                for hide in self._hide:
                    return_string += self._hide_call(hide)
            if isinstance(self._toggle_section, str):
                return_string += self._toggle_section_call(self._toggle_section)
            if is_double_list(self._toggle_sections):
                return_string += self._toggle_sections_call(self._toggle_sections[0],
                                                            self._toggle_sections[1])
            elif isinstance(self._toggle_sections, list):
                for toggle_section in self._toggle_sections:
                    if is_double_list(toggle_section):
                        return_string += self._toggle_sections_call(toggle_section[0],
                                                                    toggle_section[1])
            return_string += '"'
            return return_string
        else:
            return ""


    def _show_call(self, value: str) -> str:
        '''Returns the JS function for show'''
        return "$('#" + value + "_section').show();"


    def _hide_call(self, value: str) -> str:
        '''Returns the JS function for hide'''
        return "$('#" + value + "_section').hide();"


    def _toggle_section_call(self, value: str) -> str:
        '''returns the JS function for toggle section'''
        return "ToggleSection('" + value + "');"


    def _toggle_sections_call(self, show: list, hide: list) -> str:
        '''returns the JS function for toggle sections'''
        return "ToggleSections([" + combine(show) + "],[" + combine(hide) + "]);"


def is_double_list(var) -> bool:
    '''Checks the shape of the var '''
    if isinstance(var, tuple):
        if isinstance(var[0], list) and isinstance(var[1], list):
            return True
    return False


def combine(value: list) -> Union[str, None]:
    '''Quick Cmbine'''
    if isinstance(value, list):
        return_string = ""
        for index, item in enumerate(value):
            if index > 0:
                return_string += ", "
            return_string += "'" + item + "'"
        return return_string
    return None
