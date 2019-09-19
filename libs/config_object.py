'''Class Controller for a single Config Object'''
from libs.config_base import ConfigBase
from libs.config_option import ConfigOption
import libs.html_parts as html_part

class ConfigObject(ConfigBase):
    '''Class Controller for a single Config Object'''

    __types = ["string", "float", "string_list", "boolean", "option", "integer", "password"
               #, "ip_addr", "list", "force_list", "tuple", "int_list", "float_list",
               # "bool_list", "ip_addr_list", "mixed_list"
              ]
    __input_types = ["text", "number", "dropdown", "radio", "password", "checkbox", "multiselect",
                     "switch"
                    ]
    __special_input_types = ["checkbox", "color", "date", "datetime-local", "email",
                             "radio", "range", "text", "time", "url",
                            ]

    def __init__(self, name, label, variable_type, default=None,
                 replace_default_in_files=True, minimum=None, maximum=None, options=None,
                 input_type=None, help_text=None, script=None, button=None, button_onclick=None,
                 hide_from_html=False, read_only=False, disabled=False, priority=0, show=None,
                 hide=None, toggle_section=None, toggle_sections=None, enable_disable=None,
                 section_controller=None, not_in_config=False, value_link=None):
        '''initalise the object'''
        self.__variable_name = name.replace(" ", "").lower()
        if isinstance(variable_type, str) and variable_type in self.__types:
            self.__type = variable_type
        elif isinstance(variable_type, int) and variable_type < len(self.__types):
            self.__type = self.__types[variable_type]
        else:
            self.__type = "string"
        self.__default = default
        self.__replace_default_in_files = bool(replace_default_in_files)
        self.__minimum = minimum
        self.__maximum = maximum
        self.__options = options
        self.__input_type = input_type
        self.__help_text = help_text
        self.__button = button
        self.__button_onclick = button_onclick
        self.__not_in_config = not_in_config
        self.__value_link = value_link

        super().__init__(name, label, priority, script, hide_from_html, read_only, disabled, show,
                         hide, toggle_section, toggle_sections, enable_disable, section_controller)

    def __repr__(self):
        '''print return'''
        return "ConfigObject(" + self._name + ")"

    def default(self):
        '''return default'''
        return self.__default

    def name(self):
        '''return variable name'''
        return self._name

    def var_type(self):
        '''return variable type'''
        return self.__type

    def get_config_spec(self):
        '''Returns the line for the config option'''
        if self.__not_in_config:
            return ""
        variable_count = 0
        return_string = self._name + " = "
        if self.__type == self.__types[6]:
            return_string += self.__types[0] + "("
        else:
            return_string += self.__type + "("
        if self.__type != self.__types[3] and self.__type != self.__types[4]:
            if isinstance(self.__minimum, (int, float)):
                return_string += "min=" + str(self.__minimum)
                variable_count += 1
            if isinstance(self.__maximum, (int, float)):
                if variable_count > 0:
                    return_string += ", "
                return_string += "max=" + str(self.__maximum)
                variable_count += 1
        if isinstance(self.__options, list) and self.__type == self.__types[4]:
            for option in self.__options:
                if variable_count > 0:
                    return_string += ", "
                return_string += option.name()
                variable_count += 1
        if self.__type == self.__types[2] and self.__default is None:
            return_string += " default=list()"
        elif self.__default is not None:
            return_string += " default="
            if isinstance(self.__default, list) and self.__type == self.__types[2]:
                list_count = 0
                return_string += "list("
                for item in self.__default:
                    if list_count > 0:
                        return_string += ", "
                    if isinstance(item, bool):
                        return_string += "True" if item else "False"
                    elif isinstance(item, int):
                        return_string += item
                    elif isinstance(item, str):
                        return_string += '"' + item + '"'
                    list_count += 1
                return_string += ")"
            elif isinstance(self.__default, bool):
                return_string += "True" if self.__default else "False"
            elif isinstance(self.__default, (int, float)):
                return_string += str(self.__default)
            elif isinstance(self.__default, str):
                return_string += '"' + self.__default + '"'
        return_string += ")\n"
        return return_string

    def get_config_html(self, variable_name, value, link=None):
        '''returns the config_html'''
        if self._hide_on_html:
            return ""
        variable_name += self._name
        if value is None:
            if self.__value_link and link:
                value = self.__value_link[link][self._name]
            else:
                if isinstance(self.__default, list):
                    temp_default = []
                    for default in self.__default:
                        temp_default.append(str(default))
                    value = temp_default
                else:
                    value = str(self.__default)
        return html_part.item(variable_name, self._label, self.__help_text,
                              self.get_input_html(variable_name, value), self.__not_in_config)

    def get_input_html(self, variable_name, value):
        '''Returns the Input portion of the system'''
        if self._hide_on_html:
            return ""
        if value is None:
            value = self.__default
        if self.__button is None:
            button_html = ""
        else:
            button_html = html_part.input_button(self.__button, self.__button_onclick)
        if self.__type == self.__types[0]:
            #String
            return html_part.input_box(self.__input_types[0], variable_name, value,
                                       script=self._script_create("onchange"),
                                       max_length=self.__maximum, button=button_html,
                                       read_only=self._read_only, disabled=self._disabled)
        elif self.__type == self.__types[1]:
            #Float
            return html_part.input_box(self.__input_types[1], variable_name, value,
                                       script=self._script_create("onchange"),
                                       minimum=self.__minimum, maximum=self.__maximum,
                                       button=button_html, read_only=self._read_only,
                                       disabled=self._disabled)
        elif self.__type == self.__types[2]:
            #String List (multi select or dropdown multi or checkboxes)
            if self.__input_type is None or self.__input_type == self.__input_types[6]:
                return self.__select_box(variable_name, value, True)
            elif self.__input_type == self.__input_types[2]:
                return self.__select_box(variable_name, value, True)
            elif self.__input_type == self.__input_types[5]:
                return self.__multi_checkbox(variable_name, value)
        elif self.__type == self.__types[3]:
            #Boolean (radio or checkbox)
            if self.__input_type is None or self.__input_type == self.__input_types[3]:
                return self.__radio(variable_name, value)
            elif self.__input_type == self.__input_types[5]:
                return html_part.checkbox_single("", variable_name,
                                                 checked=value,
                                                 disabled=self._disabled,
                                                 read_only=self._read_only,
                                                 script=self._script)
            elif self.__input_type == self.__input_types[7]:
                return html_part.checkbox_switch("", variable_name,
                                                 checked=value,
                                                 disabled=self._disabled,
                                                 read_only=self._read_only,
                                                 script=self._script)
        elif self.__type == self.__types[4]:
            #Options (dropdown single or radio)
            if self.__input_type is None or self.__input_type == self.__input_types[2]:
                return self.__select_box(variable_name, value)
            elif self.__input_type == self.__input_types[3]:
                return self.__radio(variable_name, value)
        elif self.__type == self.__types[5]:
            #Integer
            return html_part.input_box(self.__input_types[1], variable_name, value,
                                       script=self._script_create("onchange"),
                                       max_length=self.__maximum, button=button_html,
                                       read_only=self._read_only, disabled=self._disabled)
        elif self.__type == self.__types[6]:
            #password
            return html_part.input_box(self.__input_types[4], variable_name, value,
                                       script=self._script_create("onchange"),
                                       button=button_html, read_only=self._read_only,
                                       disabled=self._disabled)
        # elif self.__type == self.__types[7]:
        #     #IP Address (input ipaddr])
        #     pass

        return "[BROKEN OPTION " + self._name + "]"

    def __select_box(self, variable_name, value, multiple=False):
        '''select box code'''
        options_html = ""
        for option in self.__options:
            options_html += option.html_option(value)
        return html_part.select_box(variable_name, value, options_html,
                                    read_only=self._read_only, disabled=self._disabled,
                                    multiple=multiple)

    def __radio(self, variable_name, value):
        '''Returns radio buttons'''
        return_string = ""
        for option in self.__options:
            return_string += option.html_radio(variable_name, value)
        return return_string

    def __multi_checkbox(self, variable_name, values):
        '''returns multiple checkboxes'''
        checkboxes_html = ""
        for option in self.__options:
            checkbox_bool = True if option.name() in values else False
            checkboxes_html += option.html_checkbox(variable_name, checkbox_bool)
        return checkboxes_html

    def convert_var(self, variable):
        '''Convert the variable passed in based on the type here'''
        if self.__type == self.__types[0]:
            return variable
        if self.__type == self.__types[4] or self.__type == self.__types[6]:
            return variable
        if self.__type == self.__types[5]:
            if variable == '':
                return 0
            return int(variable)
        if self.__type == self.__types[1]:
            if variable == '':
                return 0
            return float(variable)
        if self.__type == self.__types[3]:
            if isinstance(variable, str):
                if variable.lower() == "true":
                    return True
                else:
                    return False
            return bool(variable)
        if self.__type == self.__types[2]:
            clean_variable_list = []
            for var in variable:
                if "," in var:
                    split_list = var.split(",")
                    for split_var in split_list:
                        clean_variable_list.append(split_var)
                else:
                    clean_variable_list.append(var)
            return clean_variable_list
        return None

    def search_for_option_by_name(self, name):
        '''search option by name and return key to use'''
        for obj in self.__options:
            if isinstance(obj, ConfigOption):
                if obj.name() == name:
                    return obj
        return None
