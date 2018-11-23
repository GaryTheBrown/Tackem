'''Class Controller for a single Config Object'''
from libs.config_base import ConfigBase
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

    def __init__(self, name, label, variable_type, config_group=None, default=None,
                 replace_default_in_files=True, minimum=None, maximum=None, options=None,
                 input_type=None, help_text=None, script=False, button=None, button_onclick=None,
                 hide_from_html=False, readonly=False, disabled=False, priority=0, show=None,
                 hide=None, toggle_section=None, toggle_sections=None, enable_disable=None,
                 section=None, section_controller=None):
        '''initalise the object'''
        self._label = label
        self._variable_name = name.replace(" ", "").lower()
        if isinstance(variable_type, str) and variable_type in self._types:
            self._type = variable_type
        elif isinstance(variable_type, int) and variable_type < len(self._types):
            self._type = self._types[variable_type]
        else:
            self._type = "string"
        self._config_group = config_group
        self._default = default
        self._replace_default_in_files = bool(replace_default_in_files)
        self._minimum = minimum
        self._maximum = maximum
        self._options = options
        self._input_type = input_type
        self._help_text = help_text
        self._button = button
        self._button_onclick = button_onclick
        if isinstance(section, str):
            self._section = section
        else:
            self._section = ""

        super().__init__(name, priority, script, hide_from_html, readonly, disabled, show,
                         hide, toggle_section, toggle_sections, enable_disable, section_controller)

    def config_group(self, nonetostr=False):
        '''return config group'''
        if nonetostr and self._config_group is None:
            return self._name
        return self._config_group

    def section(self, nonetostr=False):
        '''return config group'''
        if nonetostr and self._section is None:
            if self._config_group is None:
                return self._name
            return self._config_group
        return self._section

    def default(self):
        '''return default'''
        return self._default

    def name(self):
        '''return variable name'''
        return self._name

    def label(self):
        '''return label'''
        return self._label

    def var_type(self):
        '''return variable type'''
        return self._type

    def get_config_section(self):
        '''Returns the line for the config option'''
        if self._name is "" and self._config_group is "plugins":
            return "$$PLUGIN_CONFIGS$$"
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

    def get_input_html(self, value=None, html_hide_override=False):
        '''returns the input html for each option'''
        if self._hide_on_html and not html_hide_override:
            return ""

        item_html = str(open("www/html/inputs/item.html", "r").read())
        item_html = item_html.replace("%%LABEL%%", self._label)
        if isinstance(self._help_text, str):
            item_html = item_html.replace("%%HELP%%", self._help_text)
        else:
            item_html = item_html.replace("%%HELP%%", '')
        item_html = item_html.replace("%%INPUT%%", self.get_only_input_html(value))
        var_name = self.get_html_var_name()
        item_html = item_html.replace("%%VARNAME%%", var_name)
        return item_html

    def get_only_input_html(self, value=None, html_hide_override=False, script=None):
        '''Returns the Input portion of the system'''
        if self._hide_on_html and not html_hide_override:
            return ""
        if value is None:
            value = self._default
        if self._type == self._types[0]:
            #String
            return self._input(self._input_types[0], value)
        elif self._type == self._types[1]:
            #Float
            return self._input(self._input_types[1], value)
        elif self._type == self._types[2]:
            #String List (multi select or dropdown multi or checkboxes)
            if self._input_type is None or self._input_type == self._input_types[6]:
                return self._select_box(True), 6
            elif self._input_type == self._input_types[2]:
                return self._select_box(True)
            elif self._input_type == self._input_types[5]:
                return self._multi_checkbox(value)
        elif self._type == self._types[3]:
            #Boolean (radio or checkbox)
            if self._input_type is None or self._input_type == self._input_types[3]:
                return self._radio(value)
            elif self._input_type == self._input_types[5]:
                return self._single_checkbox(value, False, script)
            elif self._input_type == self._input_types[7]:
                return self._single_checkbox(value, True, script)
        elif self._type == self._types[4]:
            #Options (dropdown single or radio)
            if self._input_type is None or self._input_type == self._input_types[2]:
                return self._select_box(value)
            elif self._input_type == self._input_types[3]:
                return self._radio(value)
        elif self._type == self._types[5]:
            #Integer
            return self._input(self._input_types[1], value)
        elif self._type == self._types[6]:
            #password
            return self._input(self._input_types[4], value)
        elif self._type == self._types[7]:
            #IP Address (input ipaddr])
            pass
        else:
            return "<<BROKEN OPTION " + self._name + ">>"

    def _input(self, input_type, value):
        '''A Standard input field'''
        input_html = str(open("www/html/inputs/input.html", "r").read())
        input_html = input_html.replace("%%INPUTTYPE%%", input_type)

        value_html = ""
        if input_type == self._input_types[0] or input_type == self._input_types[5]:
            if isinstance(self._maximum, int):
                maxlength_html = ' maxlength="' + str(self._maximum) + '"'
                input_html = input_html.replace("%%MAXLENGTH%%", maxlength_html)

        elif input_type == self._input_types[1]:
            if isinstance(self._minimum, int):
                min_html = ' min="' + str(self._minimum) + '"'
                input_html = input_html.replace("%%MIN%%", min_html)
            if isinstance(self._maximum, int):
                max_html = ' max="' + str(self._maximum) + '"'
                input_html = input_html.replace("%%MAX%%", max_html)
        if isinstance(value, str):
            value_html = ' value="' + value + '"'
        elif isinstance(value, (float, int)):
            value_html = ' value="' + str(value) + '"'
        elif isinstance(self._default, str) and not input_type == self._input_types[4]:
            value_html = ' value="' + self._default + '"'
        elif isinstance(self._default, (float, int)) and not input_type == self._input_types[4]:
            value_html = ' value="' + str(self._default) + '"'

        if value != "":
            input_html = input_html.replace("%%VALUE%%", value_html)

        #button stuff


        if self._button is None:
            input_html = input_html.replace(" %%BUTTON%%", "")
        else:
            button_html = str(open("www/html/inputs/inputbutton.html", "r").read())
            button_html = button_html.replace("%%BUTTONVALUE%%", self._button)
            button_html = button_html.replace("%%BUTTONONCLICK%%", self._button_onclick)
            input_html = input_html.replace("%%BUTTON%%", button_html)

        input_html = input_html.replace(" %%MAXLENGTH%%", "")
        input_html = input_html.replace(" %%MIN%%", "")
        input_html = input_html.replace(" %%MAX%%", "")
        input_html = input_html.replace(" %%VALUE%%", "")
        return self._html_input(input_html)

    def _select_box(self, value, multiple=False, box_size=0):
        '''Makes A select box'''
        box_html = str(open("www/html/inputs/blankselectedoption.html", "r").read())

        if multiple:
            box_html = box_html.replace('%%MULTIPLE%%', 'multiple')
        else:
            box_html = box_html.replace(' %%MULTIPLE%%', '')
        if box_size > 1:
            box_html = box_html.replace('%%SIZE%%', 'size="' + box_size + '"')
        else:
            box_html = box_html.replace(' %%SIZE%%', '')

        if value is None:
            options_html = str(open("www/html/inputs/blankselectedoption.html", "r").read())
        else:
            options_html = str(open("www/html/inputs/blankoption.html", "r").read())
        for option in self._options:
            options_html += option.html_option(value)

        box_html = box_html.replace("%%OPTIONS%%", options_html)

        return self._html_input(box_html, value)

    def _radio(self, value):
        '''Returns radio buttons'''
        return_string = ""
        for option in self._options:
            return_string += option.html_radio(value)
        return return_string

    def _single_checkbox(self, value, switch=False, script=None):
        '''returns a single checkbox'''
        string = str(open("www/html/inputs/singlecheckbox.html", "r").read())
        if switch:
            switch_str = str(open("www/html/inputs/switchoptions.html", "r").read())
            string = string.replace("%%SWITCH%%", switch_str)
            if script is None:
                script = "onchange=''"
            script2 = script[:-1] + 'Switch("%%VARNAME%%");' + script[-1:]
            script = script2
            #TODO add in the switch JS here but maybe keep the %%SCRIPT%% so other scripts can be added
        else:
            string = string.replace(" %%SWITCH%%", '')
        return self._html_input(string, value, script)


    def _multi_checkbox(self, value):
        '''returns a single checkbox'''
        return_string = ''
        for option in self._options:
            return_string += option.html_checkbox(value)
        return return_string

    def get_html_var_name(self):
        '''Returns the variable name for the html input'''
        var_name = "%%PLUGIN%%_"
        if isinstance(self._config_group, str) and "__" in self._config_group:
            var_name += "%%VARNAME%%_"
        else:
            if isinstance(self._config_group, str):
                var_name += self._config_group.replace(" ", "") + "_"
        var_name += self._name.replace(" ", "")
        return var_name

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
            return bool(variable)
        return None

    def get_value_var(self, plugin='', name='', instance=''):
        '''returns the uppercase var name for str.replace to use'''
        if self._type == self._types[4]:
            if self._options is None:
                return ''
            return_strings = []
            for i, _ in enumerate(self._options):
                return_string = "%%"
                return_string += plugin.upper()
                return_string += instance.upper()
                return_string += name.upper()
                if self._config_group:
                    return_string += self._config_group.replace(" ", "").upper()
                return_string += self._name.upper()
                return_string += "VALUE"
                return_string += str(i+1)
                return_string += "%%"
                return_strings.append(return_string)
            return return_strings
        else:
            return_string = "%%"
            return_string += plugin.upper()
            return_string += name.upper()
            if self._config_group:
                return_string += self._config_group.replace(" ", "").upper()
            return_string += self._name.upper()
            return_string += "VALUE%%"
            return return_string

    def get_default_string(self):
        '''returns the default value as a string'''
        if self._default is None:
            return ''
        if isinstance(self._default, str):
            return self._default
        if isinstance(self._default, (int, float)):
            return str(self._default)
        if isinstance(self._default, bool):
            if self._default:
                return "True"
            return "False"
        if isinstance(self._default, list):
            return ", ".join(self._default)
        return ""

    def get_option(self, index):
        '''returns an option'''
        return self._options[index]

    def enabled_by_controller(self, key, config_value, default_value):
        '''Search by the controller'''
        if self._options is None:
            return None
        for obj in self._options:
            if isinstance(config_value, str):
                if config_value == obj.name():
                    value = obj.show_or_hide(key)
                    if isinstance(value, bool):
                        return value
            else:
                if default_value == obj.name():
                    value = obj.show_or_hide(key)
                    if isinstance(value, bool):
                        return value
        return None
