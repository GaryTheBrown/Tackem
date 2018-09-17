'''Base class for config object and config option'''
class ConfigBase:
    '''Base Functions shared between config_object and config_option'''
    def __init__(self, name, priority, script, hide_from_html, readonly, disabled, show, hide,
                 toggle_section, toggle_sections, enable_disable, section_controller):
        self._name = name
        self._priority = priority
        self._script = script
        self._hide_on_html = hide_from_html
        self._readonly = readonly
        self._disabled = disabled
        self._show = show
        self._hide = hide
        self._toggle_section = toggle_section
        self._toggle_sections = toggle_sections
        self._enable_disable = enable_disable
        self._section_controller = section_controller

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
            if key in self._show:
                return True
        elif self._hide:
            if key in self._hide:
                return False
        return None

    def _script_create_check(self):
        '''checks if any scripts are in the option'''
        if self._show:
            return True
        if self._hide:
            return True
        if self._toggle_section:
            return True
        if self._toggle_sections:
            return True
        if self._enable_disable:
            return True
        return False

    def _script_create(self, script_call):
        '''returns the script'''
        if self._script_create_check():
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
                for toggle_sections in self._toggle_sections:
                    if is_double_list(toggle_sections):
                        return_string += self._toggle_sections_call(toggle_sections[0],
                                                                    toggle_sections[1])
            if is_triple_list(self._enable_disable):
                return_string += self._enable_disable_call(self._enable_disable[0],
                                                           self._enable_disable[1],
                                                           self._enable_disable[2])
                for enable_disable in self._enable_disable:
                    if is_triple_list(enable_disable):
                        return_string += self._enable_disable_call(enable_disable[0],
                                                                   enable_disable[1],
                                                                   enable_disable[2])
            return_string += '"'
            return return_string
        else:
            return ""

    def _show_call(self, value):
        '''Returns the JS function for show'''
        return "$('#" + value + "_section').show();"

    def _hide_call(self, value):
        '''Returns the JS function for hide'''
        return "$('#" + value + "_section').hide();"

    def _toggle_section_call(self, value):
        '''returns the JS function for toggle section'''
        return "ToggleSection('" + value + "');"

    def _toggle_sections_call(self, show, hide):
        '''returns the JS function for toggle sections'''
        return "ToggleSections([" + combine(show) + "],[" + combine(hide) + "]);"

    def _enable_disable_call(self, value, enable, set_value=None):
        '''returns the JS function for enable disable'''
        if enable:
            enable_data = "true"
        else:
            enable_data = "false"
        if set_value is True:
            set_data = "true"
        elif set_value is False:
            set_data = "false"
        else:
            set_data = "null"
        return "EnableDisable('" + value + "', " + enable_data + ", " + set_data + ");"

    def _html_input(self, string, value=None, script=None):
        if value != None:
            if isinstance(value, list):
                if self._name in value:
                    string = string.replace('%%CHECKED%%', 'checked')
                    string = string.replace('%%SELECTED%%', 'selected')
            elif isinstance(value, str):
                if value == self._name:
                    string = string.replace('%%CHECKED%%', 'checked')
                    string = string.replace('%%SELECTED%%', 'selected')
            elif isinstance(value, bool):
                if value:
                    string = string.replace('%%CHECKED%%', 'checked')
                    string = string.replace('%%SELECTED%%', 'selected')
        string = string.replace(' %%CHECKED%%', '')
        string = string.replace(' %%SELECTED%%', '')
        if self._disabled:
            string = string.replace('%%DISABLED%%', 'disabled')
        string = string.replace(' %%DISABLED%%', '')
        if self._readonly:
            string = string.replace('%%READONLY%%', 'readonly')
        string = string.replace(' %%READONLY%%', '')
        if isinstance(script, str):
            string = string.replace('%%SCRIPT%%', script)
        if isinstance(self._script, str):
            string = string.replace('%%SCRIPT%%', self._script)
        else:
            string = string.replace('%%SCRIPT%%', self._script_create("onchange"))
        string = string.replace('%%NAME%%', self._name)
        string = string.replace('%%NAMECAPITALIZE%%', self._name.capitalize())
        return string

def is_double_list(var):
    '''Checks the shape of the var '''
    if isinstance(var, tuple):
        if isinstance(var[0], list) and isinstance(var[1], list):
            return True
    return False


def is_triple_list(var):
    '''Checks the shape of the var '''
    if isinstance(var, tuple):
        if isinstance(var[0], str):
            if isinstance(var[1], bool):
                if isinstance(var[2], (bool, None)):
                    return True
    return False


def combine(value):
    '''Quick Cmbine'''
    if isinstance(value, list):
        return_string = ""
        for index, item in enumerate(value):
            if index > 0:
                return_string += ", "
            return_string += "'" + item + "'"
        return return_string
