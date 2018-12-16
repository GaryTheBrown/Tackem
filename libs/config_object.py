'''Class Controller for a single Config Object'''
from libs.config_base import ConfigBase
import libs.html_parts as html_part

class ConfigObject(ConfigBase):
    '''Class Controller for a single Config Object'''

    _types = ["string", "float", "string_list", "boolean", "option", "integer", "password"
              #, "ip_addr", "list", "force_list", "tuple", "int_list", "float_list",
              # "bool_list", "ip_addr_list", "mixed_list"
             ]
    _input_types = ["text", "number", "dropdown", "radio", "password", "checkbox", "multiselect",
                    "switch"
                   ]
    _special_input_types = ["checkbox", "color", "date", "datetime-local", "email",
                            "radio", "range", "text", "time", "url",
                           ]

    def __init__(self, name, label, variable_type, default=None,
                 replace_default_in_files=True, minimum=None, maximum=None, options=None,
                 input_type=None, help_text=None, script=False, button=None, button_onclick=None,
                 hide_from_html=False, read_only=False, disabled=False, priority=0, show=None,
                 hide=None, toggle_section=None, toggle_sections=None, enable_disable=None,
                 section_controller=None):
        '''initalise the object'''
        self._variable_name = name.replace(" ", "").lower()
        if isinstance(variable_type, str) and variable_type in self._types:
            self._type = variable_type
        elif isinstance(variable_type, int) and variable_type < len(self._types):
            self._type = self._types[variable_type]
        else:
            self._type = "string"
        self._default = default
        self._replace_default_in_files = bool(replace_default_in_files)
        self._minimum = minimum
        self._maximum = maximum
        self._options = options
        self._input_type = input_type
        self._help_text = help_text
        self._button = button
        self._button_onclick = button_onclick

        super().__init__(name, label, priority, script, hide_from_html, read_only, disabled, show,
                         hide, toggle_section, toggle_sections, enable_disable, section_controller)

    def __repr__(self):
        '''print return'''
        return "ConfigObject(" + self._name + ")"

    def default(self):
        '''return default'''
        return self._default

    def name(self):
        '''return variable name'''
        return self._name

    def var_type(self):
        '''return variable type'''
        return self._type

    def get_config_spec(self):
        '''Returns the line for the config option'''
        variable_count = 0
        return_string = self._name + " = "
        if self._type == self._types[6]:
            return_string += self._types[0] + "("
        else:
            return_string += self._type + "("
        if self._type != self._types[3] and self._type != self._types[4]:
            if isinstance(self._minimum, (int, float)):
                return_string += "min=" + str(self._minimum)
                variable_count += 1
            if isinstance(self._maximum, (int, float)):
                if variable_count > 0:
                    return_string += ", "
                return_string += "max=" + str(self._maximum)
                variable_count += 1
        if isinstance(self._options, list) and self._type == self._types[4]:
            for option in self._options:
                if variable_count > 0:
                    return_string += ", "
                return_string += option.name()
                variable_count += 1
        if self._default is not None:
            return_string += " default="
            if isinstance(self._default, list) and self._type == self._types[2]:
                list_count = 0
                return_string += "list("
                for item in self._default:
                    if list_count > 0:
                        return_string += ", "
                    elif isinstance(item, bool):
                        if item:
                            return_string += "True"
                        else:
                            return_string += "False"
                    elif isinstance(item, int):
                        return_string += item
                    elif isinstance(item, str):
                        return_string += '"' + item + '"'
                    list_count += 1
                return_string += ")"
            elif isinstance(self._default, bool):
                if self._default:
                    return_string += "True"
                else:
                    return_string += "False"
            elif isinstance(self._default, (int, float)):
                return_string += str(self._default)
            elif isinstance(self._default, str):
                return_string += '"' + self._default + '"'
        return_string += ")\n"
        return return_string

    def get_config_html(self, variable_name, value):
        '''returns the config_html'''
        if self._hide_on_html:
            return ""
        variable_name += self._name
        if value is None:
            value = str(self._default)
        return html_part.item(variable_name, self._label, self._help_text,
                              self.get_input_html(variable_name, value))

    def get_input_html(self, variable_name, value):
        '''Returns the Input portion of the system'''
        if self._hide_on_html:
            return ""
        if value is None:
            value = self._default
        if self._button is None:
            button_html = ""
        else:
            button_html = html_part.input_button(self._button, self._button_onclick)
        if self._type == self._types[0]:
            #String
            return html_part.input_box(self._input_types[0], variable_name, value,
                                       script=self._script_create("onchange"),
                                       max_length=self._maximum, button=button_html,
                                       read_only=self._read_only, disabled=self._disabled)
        elif self._type == self._types[1]:
            #Float
            return html_part.input_box(self._input_types[1], variable_name, value,
                                       script=self._script_create("onchange"),
                                       minimum=self._minimum, maximum=self._maximum,
                                       button=button_html, read_only=self._read_only,
                                       disabled=self._disabled)
        elif self._type == self._types[2]:
            #String List (multi select or dropdown multi or checkboxes)
            if self._input_type is None or self._input_type == self._input_types[6]:
                self._select_box(variable_name, value, True)
            elif self._input_type == self._input_types[2]:
                self._select_box(variable_name, value, True)
            elif self._input_type == self._input_types[5]:
                return self._multi_checkbox(variable_name, value)
        elif self._type == self._types[3]:
            #Boolean (radio or checkbox)
            if self._input_type is None or self._input_type == self._input_types[3]:
                return self._radio(variable_name, value)
            elif self._input_type == self._input_types[5]:
                return html_part.checkbox_single("", variable_name,
                                                 checked=True,
                                                 disabled=self._disabled,
                                                 read_only=self._read_only,
                                                 script=self._script_create("onchange"))
            elif self._input_type == self._input_types[7]:
                return html_part.checkbox_switch("", variable_name,
                                                 checked=True,
                                                 disabled=self._disabled,
                                                 read_only=self._read_only,
                                                 script=self._script_create("onchange"))
        elif self._type == self._types[4]:
            #Options (dropdown single or radio)
            if self._input_type is None or self._input_type == self._input_types[2]:
                self._select_box(variable_name, value)
            elif self._input_type == self._input_types[3]:
                return self._radio(variable_name, value)
        elif self._type == self._types[5]:
            #Integer
            return html_part.input_box(self._input_types[1], variable_name, value,
                                       script=self._script_create("onchange"),
                                       max_length=self._maximum, button=button_html,
                                       read_only=self._read_only, disabled=self._disabled)
        elif self._type == self._types[6]:
            #password
            return html_part.input_box(self._input_types[4], variable_name, value,
                                       script=self._script_create("onchange"),
                                       button=button_html, read_only=self._read_only,
                                       disabled=self._disabled)
        # elif self._type == self._types[7]:
        #     #IP Address (input ipaddr])
        #     pass

        return "[BROKEN OPTION " + self._name + "]"

    def _select_box(self, variable_name, value, multiple=False):
        '''select box code'''
        options_html = ""
        for option in self._options:
            options_html += option.html_option(value)
        return html_part.select_box(variable_name, value, options_html,
                                    read_only=self._read_only, disabled=self._disabled,
                                    multiple=multiple)

    def _radio(self, variable_name, value):
        '''Returns radio buttons'''
        return_string = ""
        for option in self._options:
            return_string += option.html_radio(variable_name, value)
        return return_string

    def _multi_checkbox(self, variable_name, values):
        '''returns multiple checkboxes'''
        checkboxes_html = ""
        for option in self._options:
            if option.name() in values:
                checkboxes_html += option.html_checkbox(variable_name, True)
            else:
                checkboxes_html += option.html_checkbox(variable_name, False)
        return html_part.checkbox(self._label, variable_name, checkboxes_html)

    def convert_var(self, variable):
        '''Convert the variable passed in based on the type here'''
        if self._type == self._types[0] or self._type == self._types[2]:
            return variable
        if self._type == self._types[4] or self._type == self._types[6]:
            return variable
        if self._type == self._types[5]:
            if variable == '':
                return 0
            return int(variable)
        if self._type == self._types[1]:
            if variable == '':
                return 0
            return float(variable)
        if self._type == self._types[3]:
            if isinstance(variable, str):
                if variable.lower() == "true":
                    return True
                else:
                    return False
            return bool(variable)
        return None
