'''Config List Class'''
from typing import Optional
from configobj import ConfigObj
from validate import Validator
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.config.configobj_extras import EXTRA_FUNCTIONS
from libs.config.base import ConfigBase
from libs.config.rules import ConfigRules
from libs.config.obj.base import ConfigObjBase

class ConfigList(ConfigBase):
    '''Config List Class'''

    __config = None

    def __init__(
            self,
            name: str,
            label: str,

            *objects,
            help_text: str = "",
            rules: Optional[ConfigRules] = None,
            is_section: bool = False # not in config so transparent to it. for grouping in html
        ):
        super().__init__(name, label, help_text, False, is_section, rules)

        if objects and all(not isinstance(x, (ConfigList, ConfigObjBase)) for x in objects):
            raise ValueError("objects is not all Config List or Objs")

        self.__objects = objects

        if not isinstance(is_section, bool):
            raise ValueError("rules is not a config rules object")
        self.__is_section = is_section


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
        return self.__is_section

    def find_and_set(self, location: list, value):
        '''recursive way of setting a value'''
        if len(location) == 1:
            if isinstance(self.__objects[location[0]], ConfigObjBase):
                self.__objects[location[0]].value = value
                return
        if isinstance(self.__objects[location[0]], ConfigList):
            self.__objects[location[0]].set(location[1:], value)


    def find_and_get(self, location: list):
        '''recursive way of setting a value'''
        if len(location) == 1:
            if isinstance(self.__objects[location[0]], ConfigObjBase):
                return self.__objects[location[0]].value
        if isinstance(self.__objects[location[0]], ConfigList):
            return self.__objects[location[0]].set(location[1:])
        return None


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
            self.__config.write(outfile=PROGRAMCONFIGLOCATION + "config.ini")
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
                    if not isinstance(config[item.var_name], list):
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
                item.value = config[item.var_name]


    def get_plugin_spec(self, single_instance: bool) -> str:
        '''returns the plugins generated spec file'''
        indent = 2
        return_string = self.__tab(indent) + self.__open_bracket(indent + 1)
        return_string += self.var_name + self.__close_bracket(indent + 1) + "\n"
        indent += 1
        if not single_instance:
            return_string += self.__tab(indent) + self.__open_bracket(indent + 1)
            return_string += "__many__" + self.__close_bracket(indent + 1) + "\n"
            indent += 1
        return_string += self.get_spec_part(indent)

        return return_string


    def get_spec_part(self, indent: int) -> str:
        '''function for recursion of list'''
        return_string = ""

        if self.rules is not None and isinstance(self.rules, ConfigRules):
            if self.rules.many():
                return_string += self.__tab(indent) + self.__open_bracket(indent + 1)
                return_string += "__many__" + self.__close_bracket(indent + 1) + "\n"
                indent += 1


        for item in self.__objects:
            if isinstance(item, ConfigList):
                if item.not_in_config:
                    return_string += item.get_spec_part(indent)
                else:
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


    def item_html(self) -> str:
        '''Returns the html for the config option'''
