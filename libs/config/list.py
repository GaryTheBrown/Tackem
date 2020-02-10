'''Config List Class'''
import copy
from typing import Optional
from configobj import ConfigObj
from validate import Validator
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.config.configobj_extras import EXTRA_FUNCTIONS
from libs.config.base import ConfigBase
from libs.config.rules import ConfigRules
from libs.config.obj.base import ConfigObjBase
from libs.config.obj.data.input_attributes import InputAttributes
from libs.html_system import HTMLSystem

class ConfigList(ConfigBase):
    '''Config List Class'''

    __config = None

    def __init__(
            self,
            var_name: str,
            label: str,

            *objects,
            help_text: str = "",
            rules: Optional[ConfigRules] = None,
            is_section: bool = False, # not in config so transparent to it. for grouping in html
            section_link_hide: bool = False,
            many_section=None
        ):
        if is_section and not isinstance(is_section, bool):
            raise ValueError("Is Section is not a bool")
        super().__init__(var_name, label, help_text, False, is_section, rules)

        if objects:
            if var_name == "root":
                if all(not isinstance(x, ConfigList) for x in objects):
                    raise ValueError("objects is not all Config Lists")
            elif all(not isinstance(x, (ConfigList, ConfigObjBase)) for x in objects):
                raise ValueError("objects is not all Config Lists or Objs")
        if objects:
            self.__objects = objects
        else:
            self.__objects = []

        if section_link_hide and not isinstance(section_link_hide, bool):
            raise ValueError("Section Link Hide is not a bool")
        self.__section_link_hide = section_link_hide

        if many_section and not isinstance(many_section, ConfigList):
            raise ValueError("Many Section is not a config List object or None")
        self.__many_section = many_section


    def __getitem__(self, key):
        if isinstance(key, int):
            return self.__objects[key]
        for obj in self.__objects:
            if obj.key == key.lower():
                return obj
        return None


    def __iter__(self):
        return iter(self.__objects)


    def __len__(self):
        return len(self.__objects)


    def keys(self):
        '''returns all keys for the objects'''
        return [x.var_name for x in self.__objects]

    def append(self, obj):
        '''appends the object to the list'''
        if not isinstance(obj, ConfigList) and not isinstance(obj, ConfigObjBase):
            raise ValueError("object is not a config Object")
        self.__objects.append(obj)


    def delete(self, key: str) -> bool:
        '''removed the config object according to var_name'''
        for i, obj in enumerate(self.__objects):
            if obj.key == key.lower():
                del self.__objects[i]
                return True
        return False

    def clear(self):
        '''removes all sub objects'''
        for item in self.__objects:
            if isinstance(item, ConfigList):
                item.clear()
                continue
            if isinstance(item, ConfigObjBase):
                del item
                continue
            print("error with", self.var_name, "clear Func")
        del self.__objects


    @property
    def count(self) -> int:
        '''returns the count of the config objects'''
        return len(self.__objects)


    @property
    def is_section(self) -> bool:
        '''returns if the list is a section'''
        return self.not_in_config


    @property
    def section_link_hide(self) -> bool:
        '''returns if the section link should start hidden (javascript will show it on page load'''
        return self.__section_link_hide


    @property
    def many_section(self):
        '''returns the Many Section'''
        return self.__many_section


    def clone_many_section(self, var_name: str):
        '''Clones the Many Section For Multi Instance config sections'''
        if self.many_section:
            new = copy.deepcopy(self.__many_section)
            new.label = var_name.capitalize()
            new.var_name = var_name.lower()
            self.append(new)


    def load(self):
        """Create a config file using a configspec and validate it against a Validator object"""
        temp_spec = self.get_spec_part(0)
        spec = temp_spec.split("\n")
        self.__config = ConfigObj(PROGRAMCONFIGLOCATION + "config.ini", configspec=spec)
        validator = Validator(EXTRA_FUNCTIONS)
        self.__config.validate(validator, copy=True)
        self.__config.filename = PROGRAMCONFIGLOCATION + "config.ini"

        self.load_configobj()


    def save(self):
        '''Save the Config'''
        self.update_configobj()
        try:
            print("SAVING CONFIG...")
            self.__config.write()
        except OSError:
            print("ERROR WRITING CONFIG FILE")


    def update_configobj(self, config=None):
        '''Updates the config Object for saving'''
        if self.__objects is None:
            return

        if config is None:
            config = self.__config


        for item in self.__objects:
            if isinstance(item, ConfigList):
                if item.is_section:
                    item.update_configobj(config)
                else:
                    if not item.var_name in config:
                        self.__config[item.var_name] = {}
                    item.update_configobj(config[item.var_name])
            else:
                config[item.var_name] = item.value


    def load_configobj(self, config=None):
        '''Loads the congfig object into the master config file'''
        if self.__objects is None:
            return

        if config is None:
            config = self.__config

        for item in self.__objects:
            if isinstance(item, ConfigList):
                if item.is_section:
                    item.load_configobj(config)
                else:
                    item.load_configobj(config[item.var_name])
            else:
                if item.var_name in config:
                    item.value = config[item.var_name]


    def get_spec_part(self, indent: int) -> str:
        '''function for recursion of list'''
        return_string = ""

        if self.__many_section:
            return_string += self.__tab(indent) + self.__open_bracket(indent + 1)
            return_string += "__many__" + self.__close_bracket(indent + 1) + "\n"
            return_string += self.many_section.get_spec_part(indent + 1)
        else:
            for item in self.__objects:
                if item.not_in_config:
                    continue
                if isinstance(item, ConfigList):
                    return_string += self.__tab(indent) + self.__open_bracket(indent + 1)
                    return_string += item.var_name + self.__close_bracket(indent + 1) + "\n"
                    return_string += item.get_spec_part(indent + 1)
                elif isinstance(item, ConfigObjBase):
                    return_string += self.__tab(indent) + item.spec

        return return_string


    def __tab(self, count: int) -> str:
        '''Insert the tabbing'''
        return_string = ""
        for _ in range(count):
            return_string += "    "
        return return_string


    def __open_bracket(self, count: int) -> str:
        '''Insert the open brackets'''
        return_string = ""
        for _ in range(count):
            return_string += "["
        return return_string


    def __close_bracket(self, count: int) -> str:
        '''Insert the close brackets'''
        return_string = ""
        for _ in range(count):
            return_string += "]"
        return return_string


    def html(self, variable_name: str = "") -> str:
        '''Returns the html for the config option'''
        if variable_name == "":
            if self.var_name == "root":
                return self.__root_html()
        if self.var_name == "plugin":
            return ""
        if self.is_section:
            return self.__section(variable_name)
        return self.__section(variable_name)


    def __root_html(self) -> str:
        '''Returns the html for the config option'''
        page = HTMLSystem.part(
            "pages/configpage",
            NAV=HTMLSystem.part(
                "section/tabbar",
                TABBARITEMS=self.__root_tab_bar_items(),
            ),
            HTML=self.__root_tab_panes(),
        )

        if HTMLSystem.setting("post_save"):
            return HTMLSystem.part(
                "section/form",
                RETURNURL="config",
                BUTTONLABEL="Save",
                PAGE=page,
            )
        return page


    def __root_tab_bar_items(self) -> str:
        '''Generates tab bar Item Html'''
        html = ""
        first = True
        for obj in self.__objects:
            if not isinstance(obj, ConfigList):
                continue
            html += HTMLSystem.part(
                "section/tabbaritem",
                NAME=obj.var_name,
                ACTIVE="active" if first else "",
                LABEL=obj.label
            )
            first = False
        return html


    def __root_tab_panes(self) -> str:
        '''Generates the Tab Pane'''
        single_html = ""
        panels_html = ""
        first = True
        for obj in self.__objects:
            if not isinstance(obj, ConfigList):
                single_html += obj.html()
                continue

            panels_html += HTMLSystem.part(
                "section/tabpane",
                NAME=obj.var_name,
                ACTIVE="active" if first else "",
                HTML=obj.html(obj.var_name),
            )
            first = False
        return single_html + panels_html


    def __single_panel(self, variable_name: str) -> str:
        '''Generates a Single Instance Setion/Panel'''
        return HTMLSystem.part(
            "section/panel",
            CONTROL=self.__controls(variable_name, False),
            MODAL="",#possibley none
            VARIABLENAME=variable_name,
            SECTIONHIDE=self.__section_hide(),
            SECTION=self.__section_data(variable_name, True)
        )


    def __multi_panel(self, variable_name: str) -> str:
        '''Generates a Multi Instance Setion/Panel'''
        return HTMLSystem.part(
            "section/panel",
            CONTROL=self.__controls(variable_name, True),
            MODAL="", #TODO its own class in config to set it up. act like a list
            VARIABLENAME=variable_name,
            SECTIONHIDE=self.__section_hide(),
            SECTION=self.__section_data(variable_name, True)
        )


    def __section_data(self, variable_name, hide_controls: bool = False):
        '''pulls all objects out for inclusion in the section'''
        html = ""
        for obj in self.__objects:
            if hide_controls and (obj.var_name == "enabled" or obj.var_name == "disabled"):
                continue
            html += obj.html(variable_name)
        return html


    def __controls(self, variable_name: str, multi: bool) -> str:
        '''creates the control buttons'''
        html = ""
        for obj in self.__objects:
            if obj.var_name == "enabled" or obj.var_name == "disabled":
                html += obj.item_html(variable_name)
                break
        if multi:
            variables = variable_name.split("_")
            input_attributes = InputAttributes(
                action="delete_multi_plugin",
                data_plugin_type=variables[1],
                data_plugin_name=variables[2],
                data_plugin_instance=self.var_name
                ).html()

            html += HTMLSystem.part(
                "input/button",
                BUTTONVALUE="Delete",
                DATA=input_attributes
            )

        return html


    def __section(self, variable_name: str) -> str:
        '''creates an Invisible to html section'''
        var = "{}_{}".format(variable_name, self.var_name) if variable_name != "" else self.var_name
        section_html = HTMLSystem.part(
            "section/section",
            SECTIONNAME=var,
            SECTIONHIDE=self.__section_hide(),
            SECTION=self.__section_data(variable_name)
        )
        return section_html


    def __section_hide(self) -> str:
        '''returns string to hide section if it should be hidden'''
        # hide_html = 'style="display:none;"'
        # if "enabled" in self.keys():
        #     if not self.__getitem__("enabled").value:
        #         return hide_html
        #     return ""
        # if "disabled" in self.keys():
        #     if self.__getitem__("disabled").value:
        #         return hide_html
        #     return ""
        # if self.__section_link_hide:
        #     return hide_html

        return ""
