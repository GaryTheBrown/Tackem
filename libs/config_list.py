'''Class Controller for Config Object list'''
from collections import OrderedDict
from libs.config_object import ConfigObject

class ConfigList:
    '''Class Controller for Config Object list'''
    def __init__(self, plugin_name, plugin, group_priorities=None):
        self._config_objects = []
        self._javascript_functions = []
        self._plugin_name = plugin_name
        self._plugin = plugin
        if group_priorities is None:
            self._group_priorities = {}
        else:
            self._group_priorities = group_priorities

    def __repr__(self):
        '''print return'''
        return "ConfigList(" + self._plugin_name + ")"
        #TODO ADD THIS ALL OVER

    def append(self, config_object, javascript_function=None):
        '''append item to the list'''
        self._config_objects.append(config_object)
        if isinstance(javascript_function, str):
            self._javascript_functions.append(javascript_function)

    def append_config(self, config_object):
        '''append item to the list'''
        self._config_objects.append(config_object)

    def append_priority(self, group, value):
        '''append a group priority'''
        self._group_priorities.set(group, value)

    def append_javascript(self, javascript_function):
        '''append item to the list'''
        self._javascript_functions.append(javascript_function)

    def sort_config(self):
        '''Sort the list Test'''
        self._config_objects.sort(key=lambda x: (x.priority(),
                                                 x.section(True),
                                                 x.config_group(True),
                                                 x.name()))

    def get_cfg(self, plugin_name):
        '''Returns the CFG for the plugin'''
        sorted_root_data, sorted_data = self._fetch_data_cfg()
        return_string = ""
        if plugin_name != "":
            return_string += "\n" + self._tab(2) + "[[" + plugin_name + "]]\n"
            for item in sorted_root_data:
                return_string += self._tab(3) + sorted_root_data[item]
            for group_item in sorted_data:
                return_string += self._tab(3) + "[[[" + group_item + "]]]\n"
                for item in sorted_data[group_item]:
                    return_string += self._tab(4) + sorted_data[group_item][item]
        else:
            for item in sorted_root_data:
                return_string += self._tab(1) + sorted_root_data[item]
            for group_item in sorted_data:
                return_string += "\n" + self._tab(1) + "[" + group_item + "]\n"
                for item in sorted_data[group_item]:
                    return_string += self._tab(2) + sorted_data[group_item][item]

        return return_string

    def _tab(self, count):
        '''Insert the tabbing'''
        return_string = ""
        for _ in range(count):
            return_string += "    "
        return return_string

    def get_multi_html_options(self, config):
        '''Returns the __many__ Data'''
        data = self._fetch_data_html(config)
        multi_html_box = str(open("www/html/inputs/multiplugin.html", "r").read())
        enabled_html = ""
        partname = self._plugin_name + "_%%VARNAME%%"
        if "enabled" in data["__many__"]:
            enabled_html = self.fetch_enabled_html(True, "__many__", False)
            varname = partname + "_enabled"
            enabled_html = enabled_html.replace("%%VARNAME%%", varname)
        multi_html_box = multi_html_box.replace("%%ENABLEDOPTION%%", enabled_html)
        delete_html = str(open("www/html/inputs/deleteinstancebutton.html", "r").read())
        multi_html_box = multi_html_box.replace("%%DELETEOPTION%%", delete_html)
        multi_html_box = multi_html_box.replace("%%PARTNAME%%", partname)

        hide_string = ""
        if not self.get_default("__many__", 'enabled', True):
            hide_string = 'style="display:none;"'
        multi_html_box = multi_html_box.replace("%%PLUGINSECTIONHIDE%%", hide_string)
        options = ""
        for key, item in data["__many__"].items():
            if key == "enabled":
                continue
            options += item
        multi_html_box = multi_html_box.replace("%%OPTIONS%%", options)
        multi_html_box = multi_html_box.replace("%%PLUGINNAME%%", self._plugin_name)
        return multi_html_box

    def get_only_html_options(self, config):
        '''returns the HTML options Section to use'''
        data = self._fetch_data_html(config)
        full_html = ""
        temp_section_html = ""
        last_section = ""
        #first grab all root configs
        for key, item in data.items():
            if key == "enabled" or "__" in key:
                continue
            if self._plugin_name == "root" and key == "plugins":
                continue
            if isinstance(item, OrderedDict):
                continue

            i = self.search_by_group_and_name(None, key)
            section = self._config_objects[i].section()
            if last_section != "" and section != last_section: # section change over
                full_html += self._make_section(last_section, temp_section_html, config)
                temp_section_html = ''
            if section == "":#No Section
                full_html += item
            else: # Section
                temp_section_html += item
            last_section = section

        if temp_section_html != "":
            full_html += self._make_section(last_section, temp_section_html, config)
            temp_section_html = ''
        #then loop through each group
        for key, item in data.items():
            if key == "enabled" or "__" in key:
                continue
            if self._plugin_name == "root" and key == "plugins":
                continue
            if isinstance(item, str):
                continue

            plugin_html = ""
            temp_section_html = ""
            last_section = ""
            enabled_in_section = False
            for o_key, obj in item.items():
                if o_key == "enabled":
                    enabled_in_section = True
                    continue
                i = self.search_by_group_and_name(key, o_key)
                section = self._config_objects[i].section()
                if last_section != "" and section != last_section: # section change over
                    plugin_html += self._make_section(last_section, temp_section_html, config)
                    temp_section_html = ''
                if section == "":#No Section
                    plugin_html += obj
                else: # Section
                    temp_section_html += obj
                last_section = section
            if temp_section_html != "":
                plugin_html += self._make_section(last_section, temp_section_html, config)
                temp_section_html = ''

            plugin = str(open("www/html/inputs/plugin.html", "r").read())
            plugin = plugin.replace("%%PLUGINSECTION%%", plugin_html)

            if enabled_in_section:#ENABLED SECTION
                enabled_default = self.get_default("", "enabled", True)
                enabled_data = config.get(key, {}).get('enabled', enabled_default)
                plugin_onoff = self.fetch_enabled_html(enabled_data, key)
                plugin_onoff = plugin_onoff.replace("%%PLUGIN%%", key)
                plugin_onoff = plugin_onoff.replace("%%VARNAME%%", key + "_enabled")
                plugin_onoff = plugin_onoff.replace("_%%NAME%%", "")
                plugin = plugin.replace("%%CONTROL%%", plugin_onoff)
            else:#NO ENABLED SECTION
                plugin = plugin.replace("%%CONTROL%%", "")

            plugin = plugin.replace("%%PLUGINNAME%%", key)
            plugin = plugin.replace("%%MODAL%%", "")
            replacement_var = ""
            if not config.get(key, {}).get('enabled', self.get_default("", "enabled", True)):
                replacement_var = 'style="display:none;"'
            full_html += plugin.replace(" %%PLUGINSECTIONHIDE%%", replacement_var)

        return full_html

    def _make_section(self, last_section, temp_section_html, config):
        '''Creates the Section'''
        section_html = str(open("www/html/inputs/section.html", "r").read())
        section_html = section_html.replace("%%SECTIONNAME%%", last_section)
        section_html = section_html.replace("%%SECTION%%", temp_section_html)
        replacement_var = ""
        if not self._enabled_by_controller(last_section, config):
            replacement_var = 'style="display:none;"'
        return section_html.replace("%%SECTIONHIDE%%", replacement_var)

    def fetch_enabled_html(self, enabled=None, group=None, single_instance=True):
        '''will return the enabled option'''
        #data = self._fetch_data_single()
        location = self.search_by_group_and_name(group, "enabled")
        if location is None:
            return ""
        if single_instance:
            script = "onchange='ToggleSection(\"%%PLUGIN%%\");'"
        else:
            script = "onchange='ToggleSection(\"%%PARTNAME%%\");'"
        return_string = self._config_objects[location].get_only_input_html(enabled, script=script)
        return return_string

    def _fetch_data(self):
        '''Sorts the config Data and returns 2 sorted dicts for running through'''
        root_data = OrderedDict()
        data = OrderedDict()
        for config_object in self._config_objects:
            group = config_object.config_group()
            name = config_object.name()
            if group is None:
                root_data[name] = config_object
            elif isinstance(group, str):
                if not group in data:
                    data[group] = OrderedDict()
                data[group][name] = config_object
        return root_data, data

    def _fetch_data_single(self):
        '''Sorts the config Data and returns 2 sorted dicts for running through'''
        data = OrderedDict()
        for config_object in self._config_objects:
            group = config_object.config_group()
            name = config_object.name()
            if group is None:
                data[name] = config_object
            elif isinstance(group, str):
                if not group in data:
                    data[group] = OrderedDict()
                if isinstance(data[group], OrderedDict):
                    data[group][name] = config_object
        return data

    def _fetch_data_cfg(self):
        '''Sorts the config Data and returns 2 sorted dicts for running through'''
        root_data, data = self._fetch_data()
        for item in root_data:
            root_data[item] = root_data[item].get_config_section()
        for group in data:
            for item in data[group]:
                data[group][item] = data[group][item].get_config_section()
        return root_data, data

    def _fetch_data_html(self, config):
        '''returns 2 sorted dicts for running through'''
        data = self._fetch_data_single()
        return_data = OrderedDict()

        for key_group, group in data.items():
            if isinstance(group, OrderedDict):
                return_data[key_group] = OrderedDict()
                for key_item, item in group.items():
                    temp_value = config.get(key_group, {})
                    if isinstance(temp_value, dict):
                        value = temp_value.get(key_item)
                    else:
                        value = temp_value
                    return_data[key_group][key_item] = item.get_input_html(value)
            elif isinstance(group, ConfigObject):
                value = config.get(key_group)
                return_data[key_group] = group.get_input_html(value)
        return return_data

    def single_instance_load(self, config):
        '''Loads the single instance html ready for the options to be injected'''
        plugin = str(open("www/html/inputs/plugin.html", "r").read())
        plugin_options = self.get_only_html_options(config)
        plugin = plugin.replace("%%PLUGINSECTION%%", plugin_options)
        plugin_onoff = self.fetch_enabled_html(config.get('enabled',
                                                          self.get_default("", "enabled", True)))
        plugin_onoff = plugin_onoff.replace("%%VARNAME%%", self._plugin_name + "_enabled")
        plugin_onoff = plugin_onoff.replace("_%%NAME%%", "")
        plugin = plugin.replace("%%CONTROL%%", plugin_onoff)
        plugin = plugin.replace("%%PLUGIN%%", self._plugin_name)
        plugin = plugin.replace("%%PLUGINNAME%%", self._plugin_name)
        plugin = plugin.replace("%%MODAL%%", "")
        replacement_var = ""
        if not config.get('enabled', self.get_default("", "enabled", True)):
            replacement_var = 'style="display:none;"'
        plugin = plugin.replace(" %%PLUGINSECTIONHIDE%%", replacement_var)
        return plugin

    def multi_instance_load(self):
        '''Loads the multi instance html and modals needed ready for the options to be injected'''
        settings = self._plugin.SETTINGS
        plugin = str(open("www/html/inputs/plugin.html", "r").read())
        if 'list_of_options' in settings:
            modal_multi_list = str(open("www/config/list_modal.html", "r").read())
            options = self._select_box(self._plugin_name + "_name", settings['list_of_options'])
            plugin = plugin.replace("%%MODAL%%", modal_multi_list.replace("%%LIST%%", options))
        else:
            modal_multi = str(open("www/config/multi_modal.html", "r").read())
            plugin = plugin.replace("%%MODAL%%", modal_multi)
        button = str(open("www/html/inputs/addinstancebutton.html", "r").read())
        plugin = plugin.replace("%%CONTROL%%", button)
        replacement_var = ''
        if not self.get_default("__many__", "enabled", True):
            replacement_var = 'style="display:none;"'
        plugin = plugin.replace(" %%PLUGINSECTIONHIDE%%", replacement_var)
        plugin = plugin.replace("%%PLUGINNAME%%", self._plugin_name)
        plugin = plugin.replace("%%PLUGINSECTION%%", "%%" + self._plugin_name.upper() + "SECTION%%")
        return plugin.replace("%%TITLE%%", self._plugin_name.capitalize())

    def _select_box(self, name, list_of_options):
        '''Makes A select box'''
        select_box = str(open("www/html/inputs/selectbox.html", "r").read())
        select_box = select_box.replace("%%VARNAME%%", name.replace(" ", ""))
        select_box = select_box.replace(" %%MULTIPLE%%", '')
        select_box = select_box.replace(" %%SIZE%%", '')
        select_box = select_box.replace(" %%SCRIPT%%", '')
        select_box = select_box.replace(" %%READONLY%%", '')
        select_box = select_box.replace(" %%DISABLED%%", '')
        options = str(open("www/html/inputs/blankselectedoption.html", "r").read())
        option_start_html = str(open("www/html/inputs/option.html", "r").read())
        for option in list_of_options:
            option_html = option_start_html.replace("%%NAME%%", option)
            option_html = option_html.replace("%%NAMECAPITALIZE%%", option.capitalize())
            option_html = option_html.replace(" %%SELECTED%%", '')
            option_html = option_html.replace(" %%DISABLED%%", '')
            option_html = option_html.replace(" %%READONLY%%", '')
            option_html = option_html.replace(" %%SCRIPT%%", '')
            options += option_html
        select_box = select_box.replace("%%OPTIONS%%", options)
        return select_box

    def search_by_name(self, name):
        '''search by name and return key to use'''
        for i, obj in enumerate(self._config_objects):
            if obj.name() == name:
                return i
        return None

    def search_by_group(self, group):
        '''search by name and return key to use'''
        for i, obj in enumerate(self._config_objects):
            if obj.config_group() == group:
                return i
        return None

    def search_by_group_and_name(self, group, name):
        '''search by name and return key to use'''
        for i, obj in enumerate(self._config_objects):
            if obj.config_group() == group and obj.name() == name:
                return i
        return None

    def _enabled_by_controller(self, key, config):
        '''Search by the controller'''
        for obj in self._config_objects:
            default_value = obj.default()
            config_value = config.get(obj.config_group(), {}).get(obj.name(), None)
            if obj.section_controller() == key:
                if isinstance(default_value, bool):
                    if config_value is None:
                        return default_value
                    else:
                        return config_value
            else:
                section_controller = obj.enabled_by_controller(key, config_value, default_value)
                if section_controller is not None:
                    return section_controller
        return True # any problen return true so section is displayed

    def get_default(self, group, name, default=None):
        '''search and return default'''
        count = self.search_by_group_and_name(group, name)
        if count is None:
            return default
        return self._config_objects[count].default()

    def convert_var(self, group, name, variable):
        '''search and return type'''
        count = self.search_by_group_and_name(group, name)
        if count is None:
            return None
        return self._config_objects[count].convert_var(variable)

    def get_list_of_vars_and_defaults(self, plugin='', name=''):
        '''Creates a dict of data for replace to use to place the defaults'''
        return_dict = {}
        for option in self._config_objects:
            return_data = option.get_value_var(plugin, name)
            default = option.get_default_string()
            return_dict.update(self._sort_return_data(return_data, default, option))

        return return_dict

    def get_list_of_vars_and_values(self, config_dict, plugin='', name=''):
        '''Creates a dict of data for replace to use to place the defaults'''
        return_dict = {}

        groups = self.get_groups()

        for option in self._config_objects:
            item_group = option.config_group()
            item_name = option.name()
            value = None
            values = {}
            if item_group:
                if item_group.lower() == "__many__":
                    for item in config_dict:
                        if item in groups:
                            continue
                        if isinstance(config_dict[item], list):
                            values[item] = config_dict.get(item, {}).get(item_name, None)

                else:
                    value = config_dict.get(item_group, {}).get(item_name, None)
            else:
                value = config_dict.get(item_name, None)

            if values:
                for item in values:
                    return_data = option.get_value_var(plugin, name, item)
                    if value is None:
                        default = option.get_default_string()
                        return_dict.update(self._sort_return_data(return_data, default, option))
                    else:
                        return_dict.update(self._sort_return_data(return_data, item, option))

            else:
                return_data = option.get_value_var(plugin, name)
                if value is None:
                    default = option.get_default_string()
                    return_dict.update(self._sort_return_data(return_data, default, option))
                else:
                    return_dict.update(self._sort_return_data(return_data, value, option))

        return return_dict

    def _sort_return_data(self, return_data, value, option):
        '''sends out return data as strings ready for html use'''
        return_dict = {}

        if isinstance(return_data, list):
            for index, item in enumerate(return_data):
                if value == option.get_option(index).name():
                    return_dict[item] = "checked"
                else:
                    return_dict[item] = ""
        elif isinstance(return_data, str):
            if isinstance(value, str) and value == "True":
                return_dict[return_data] = "checked"
            elif isinstance(value, bool) and value:
                return_dict[return_data] = "checked"
            elif isinstance(value, str) and value == "False":
                return_dict[return_data] = ""
            elif isinstance(value, bool) and not value:
                return_dict[return_data] = ""
            elif isinstance(value, str):
                return_dict[return_data] = value
            elif isinstance(value, (int, float)):
                return_dict[return_data] = value

        return return_dict

    def get_groups(self):
        '''Returns a list of the Groups'''
        groups = []
        for option in self._config_objects:
            if not option.config_group() in groups and not option.config_group() == "__many__":
                groups.append(option.config_group())

        return groups
