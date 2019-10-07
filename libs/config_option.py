'''Object for holding variables for the config object but is also a base class of the config_object
   becasue of shared code and functions'''
from libs.config_base import ConfigBase
import libs.html_parts as html_part


class ConfigOption(ConfigBase):
    '''Class to hold variables for options'''


    def __init__(self, name, label, priority=0, script=None, hide_from_html=False, read_only=False,
                 disabled=False, show=None, hide=None, toggle_section=None, toggle_sections=None,
                 enable_disable=None, section_controller=None):
        super().__init__(name, label, priority, script, hide_from_html, read_only, disabled, show,
                         hide, toggle_section, toggle_sections, enable_disable, section_controller)


    def name(self):
        '''returns the name for cfg.'''
        return self._name


    def html_option(self, value=None):
        ''' returns a html option'''
        return html_part.select_box_option(self._name, self._label, value == self._name,
                                           read_only=self._read_only, disabled=self._disabled,
                                           script=self._script_create("onchange"))


    def html_radio(self, variable_name, value=None):
        ''' returns a html radio button'''
        return html_part.radio_option(variable_name, self._name, self._label, value == self._name,
                                      disabled=self._disabled, read_only=self._read_only,
                                      script=self._script_create("onchange"))


    def html_checkbox(self, variable_name, checked=False):
        '''returns a checkbox'''
        return html_part.checkbox_multi(self._label, variable_name, self._name,
                                        checked=checked, disabled=self._disabled,
                                        read_only=self._read_only,
                                        script=self._script_create("onchange"))
