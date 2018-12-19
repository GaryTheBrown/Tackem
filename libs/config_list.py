'''Class Controller for Config Object list'''
from libs.config_object import ConfigObject
from libs.config_rules import ConfigRules
import libs.html_parts as html_part

class ConfigList:
    '''Class Controller for Config Object list'''
    def __init__(self, name, plugin=None, objects=None, rules=None, javascripts=None,
                 is_section=False, section_link=None):
        if isinstance(name, str):
            self._name = name
        if isinstance(plugin, str):
            self._plugin = plugin
        self._objects = []
        if isinstance(objects, (ConfigObject, ConfigList)):
            self._objects.append(objects)
        elif isinstance(objects, list):
            self._objects = objects
        self._rules = None
        if isinstance(rules, ConfigRules):
            self._rules = rules
        self._javascripts = []
        if isinstance(javascripts, str):
            self._javascripts.append(javascripts)
        elif isinstance(javascripts, list):
            self._javascripts = javascripts
        self._is_section = is_section
        self._section_link = section_link

    def __repr__(self):
        '''print return'''
        return "ConfigList(" + self._name + ")"

    def append(self, config_object):
        '''append item to the list'''
        if isinstance(config_object, (ConfigObject, ConfigList)):
            self._objects.append(config_object)

    def append_javascript(self, javascript_function):
        '''append item to the list'''
        if isinstance(javascript_function, str):
            self._javascripts.append(javascript_function)

    def name(self):
        '''get name'''
        return self._name

    def objects(self):
        '''get objects'''
        return self._objects

    def rules(self):
        '''get rules'''
        return self._rules

    def is_section(self):
        '''get if is section'''
        return self._is_section

    def section_link(self):
        '''get link to rules for the section'''
        return self._section_link

    def get_root_spec(self):
        '''returns the root generated spec file'''
        return self._get_spec_part(self._objects, 0)

    def get_plugin_spec(self, single_instance):
        '''returns the plugins generated spec file'''
        indent = 2
        return_string = self._tab(indent) + self._open_bracket(indent + 1)
        return_string += self._name + self._close_bracket(indent + 1) + "\n"
        indent += 1
        if not single_instance:
            return_string += self._tab(indent) + self._open_bracket(indent + 1)
            return_string += "__many__" + self._close_bracket(indent + 1) + "\n"
            indent += 1
        return return_string + self._get_spec_part(self._objects, indent)

    def _get_spec_part(self, config_list, indent):
        '''function for recursion of list'''
        return_string = ""
        list_to_loop = config_list
        if isinstance(config_list, ConfigList):
            list_to_loop = config_list.objects()
            if isinstance(config_list.rules(), ConfigRules) and config_list.rules().many():
                return_string += self._tab(indent) + self._open_bracket(indent + 1)
                return_string += "__many__" + self._close_bracket(indent + 1) + "\n"
                indent += 1
        else:
            if self._rules is not None and isinstance(self._rules, ConfigRules):
                if self._rules.many():
                    return_string += self._tab(indent) + self._open_bracket(indent + 1)
                    return_string += "__many__" + self._close_bracket(indent + 1) + "\n"
                    indent += 1

        for item in list_to_loop:
            if isinstance(item, ConfigList):
                return_string += self._tab(indent) + self._open_bracket(indent + 1)
                return_string += item.name() + self._close_bracket(indent + 1) + "\n"
                return_string += self._get_spec_part(item, indent + 1)

            elif isinstance(item, ConfigObject):
                return_string += self._tab(indent) + item.get_config_spec()

        return return_string

    def _tab(self, count):
        '''Insert the tabbing'''
        return_string = ""
        for _ in range(count):
            return_string += "    "
        return return_string

    def _open_bracket(self, count):
        '''Insert the open brackets'''
        return_string = ""
        for _ in range(count):
            return_string += "["
        return return_string

    def _close_bracket(self, count):
        '''Insert the close brackets'''
        return_string = ""
        for _ in range(count):
            return_string += "]"
        return return_string

    def convert_var(self, location_list, variable):
        '''search and return type'''
        if len(location_list) is 1:
            config_object = self.search_for_object_by_name(location_list[0])
            if config_object is None:
                return None
            return config_object.convert_var(variable)
        else:
            if self._rules is not None and self._rules.many():
                return self.convert_var(location_list[1:], variable)
            config_list = self.search_for_list_by_name(location_list[0])
            if config_list is None:
                return None
            return config_list.convert_var(location_list[1:], variable)

    def search_for_object_by_name(self, name):
        '''search objects by name and return key to use'''
        for obj in self._objects:
            if isinstance(obj, ConfigObject):
                if obj.name() == name:
                    return obj
        return None

    def search_for_list_by_name(self, name):
        '''search by name and return key to use'''
        for obj in self._objects:
            if isinstance(obj, ConfigList):
                if obj.name() == name:
                    return obj
        return None

    def check_if_section_is_hidden(self, config=None):
        '''checks if the list has an enabled object returns its default value if it does'''
        if config is None:
            enabled_object = self.search_for_object_by_name("enabled")
            if enabled_object is None:
                return False
            return not enabled_object.default()
        return not config.get("default", True)

    def get_config_html(self, config, variable_name="", link=None):
        '''returns the config_html'''
        return_html = ""
        for obj in self._objects:
            variable_name_loop = variable_name
            value = config.get(obj.name(), None)
            if isinstance(obj, ConfigObject):
                if obj.name() is not "enabled":
                    return_html += obj.get_config_html(variable_name_loop, value, link)
            elif isinstance(obj, ConfigList):
                if obj.name() is not "plugins":
                    variable_name_loop += obj.name() + "_"
                    temp_config = None
                    if isinstance(config, dict):
                        temp_config = config[obj.name()]
                    section_enabled = not obj.check_if_section_is_hidden(temp_config)
                    control_html = ""
                    if obj.search_for_object_by_name("enabled"):
                        control_html = html_part.checkbox_switch("enabled",
                                                                 variable_name_loop,
                                                                 section_enabled, script=True)
                    if obj.is_section():
                        visible = self.config_find(config, obj.section_link()) == obj.name()
                        return_html += html_part.section(variable_name_loop[:-1],
                                                         obj.get_config_html(temp_config,
                                                                             variable_name_loop),
                                                         visible)
                    elif isinstance(obj.rules(), ConfigRules) and obj.rules().many():
                        many_html = self._many_section(obj, temp_config, variable_name_loop)

                        return_html += html_part.panel(obj.name(), "", "",
                                                       variable_name_loop[:-1],
                                                       many_html,
                                                       True)
                    else:
                        return_html += html_part.panel(obj.name(), control_html, "",
                                                       variable_name_loop[:-1],
                                                       obj.get_config_html(temp_config,
                                                                           variable_name_loop),
                                                       section_enabled)
        return return_html

    def _many_section(self, obj, config, variable_name):
        '''Work for the Many section done here'''
        many_html = ""
        for_each = obj.rules().for_each()
        if for_each:
            if isinstance(for_each, list):
                for item in for_each:
                    variable_name_loop = variable_name + item + "_"
                    control_html = ""
                    enabled = True
                    enabled_check = obj.search_for_object_by_name("enabled")
                    if enabled_check is not None:
                        if item in config:
                            enabled = config[item].get("enabled", enabled_check)
                        control_html = html_part.checkbox_switch("enabled",
                                                                 variable_name_loop,
                                                                 enabled, script=True)

                    label = item
                    many_html += html_part.panel(label, control_html, "", variable_name_loop[:-1],
                                                 obj.get_config_html(config,
                                                                     variable_name_loop),
                                                 enabled)
            elif isinstance(for_each, dict):
                for key in for_each:
                    variable_name_loop = variable_name + key + "_"
                    control_html = ""
                    enabled = True
                    enabled_check = obj.search_for_object_by_name("enabled")
                    if enabled_check is not None:
                        if key in config:
                            enabled = config[key].get("enabled", enabled_check)
                        control_html = html_part.checkbox_switch("enabled",
                                                                 variable_name_loop,
                                                                 enabled, script=True)

                    label = key
                    if 'label' in for_each[key]:
                        label = for_each[key]['label']
                    many_html += html_part.panel(label, control_html, "", variable_name_loop[:-1],
                                                 obj.get_config_html(config, variable_name_loop,
                                                                     key), enabled)
        return many_html

    def config_find(self, config, section_link):
        '''A recursive way of finding a value from the config'''
        if isinstance(section_link, list):
            if section_link[0] in config:
                if len(section_link) is 1:
                    return config[section_link[0]]
                return self.config_find(config[section_link[0]], section_link[1:])
            return None
        return config[section_link]
