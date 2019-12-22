'''Config List Class'''
from typing import Optional
from libs.config.base import ConfigBase
from libs.config.rules import ConfigRules
from libs.config.obj.base import ConfigObjBase

class ConfigList(ConfigBase):
    '''Config List Class'''


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
        self.__objects = []

        for obj in objects:
            if not isinstance(obj, (ConfigList, ConfigObjBase)):
                raise ValueError("object is not a config Object")
            self.__objects.append(obj)

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
        if not isinstance(obj, ConfigList) and not issubclass(obj, ConfigObjBase):
            raise ValueError("object is not a config Object")
        self.__objects.append(obj)

    def delete(self, key: str) -> bool:
        '''removed the config object according to var_name'''
        for i, obj in enumerate(self.__objects):
            if obj.key == key.lower():
                del self.__objects[i]
                return True
        return False

    @property
    def count(self) -> int:
        '''returns the count of the config objects'''
        return len(self.__objects)

    @property
    def get_root_spec(self) -> str:
        '''returns the root generated spec file'''
        return self.get_spec_part(0)


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
                return_string += self.__tab(indent) + item.config_spec()

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
