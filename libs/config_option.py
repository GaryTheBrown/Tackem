'''Object for holding variables for the config object but is also a base class of the config_object
   becasue of shared code and functions'''
from libs.config_base import ConfigBase


class ConfigOption(ConfigBase):
    '''Class to hold variables for options'''

    def __init__(self, name, priority=0, script=None, hide_from_html=False, readonly=False,
                 disabled=False, show=None, hide=None, toggle_section=None, toggle_sections=None,
                 enable_disable=None, section_controller=None):
        super().__init__(name, priority, script, hide_from_html, readonly, disabled, show,
                         hide, toggle_section, toggle_sections, enable_disable, section_controller)

    def name(self):
        '''returns the name for cfg.'''
        return self._name

    def html_option(self, value=None):
        ''' returns a html option'''
        return self._html_input(str(open("www/html/inputs/option.html", "r").read()), value)

    def html_radio(self, value=None):
        ''' returns a html radio button'''
        return self._html_input(str(open("www/html/inputs/radio.html", "r").read()), value)

    def html_checkbox(self, value=None):
        '''returns a checkbox'''
        checkbox_html = str(open("www/html/inputs/checkbox.html", "r").read())
        single_checkbox_html = str(open("www/html/inputs/singlecheckbox.html", "r").read())
        html = checkbox_html.replace("%%SINGLECHECKBOX%%", single_checkbox_html)
        return self._html_input(html, value)
