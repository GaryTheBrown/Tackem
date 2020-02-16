'''Config List Class'''
import copy
from typing import Optional
from libs.config.base import ConfigBase
from libs.config.rules import ConfigRules
from libs.config.obj.base import ConfigObjBase


class ConfigListBase(ConfigBase):
    '''Config List Class'''

    def __init__(
            self,
            var_name: str,
            label: str,

            *objects,
            help_text: str = "",
            rules: Optional[ConfigRules] = None,
            is_section: bool = False,
            section_link_hide: bool = False,
            many_section=None
        ):
        super().__init__(var_name, label, help_text, False, False, rules)

        if is_section and not isinstance(is_section, bool):
            raise ValueError("Is Section is not a bool")
        self.__is_section = is_section

        if objects:
            if var_name == "root":
                if all(not isinstance(x, ConfigListBase) for x in objects):
                    raise ValueError("objects is not all Config Lists")
            elif all(not isinstance(x, (ConfigListBase, ConfigObjBase)) for x in objects):
                raise ValueError("objects is not all Config Lists or Objs")
        if objects:
            self._objects = objects
        else:
            self._objects = []

        if section_link_hide and not isinstance(section_link_hide, bool):
            raise ValueError("Section Link Hide is not a bool")
        self.__section_link_hide = section_link_hide

        if many_section and not isinstance(many_section, ConfigListBase):
            raise ValueError("Many Section is not a config List object or None")
        self.__many_section = many_section


    def __getitem__(self, key):
        if isinstance(key, int):
            return self._objects[key]
        for obj in self._objects:
            if obj.key == key.lower():
                return obj
        return None


    def __iter__(self):
        return iter(self._objects)


    def __len__(self):
        return len(self._objects)


    def keys(self):
        '''returns all keys for the objects'''
        return [x.var_name for x in self._objects]

    def get(self, key, default=None):
        '''returns the data if found otherwise returns the default value'''
        for obj in self._objects:
            if obj.key == key.lower():
                return obj
        return default


    def append(self, obj):
        '''appends the object to the list'''
        if not isinstance(obj, ConfigListBase) and not isinstance(obj, ConfigObjBase):
            raise ValueError("object is not a config Object")
        self._objects.append(obj)


    def delete(self, key: str) -> bool:
        '''removed the config object according to var_name'''
        for i, obj in enumerate(self._objects):
            if obj.key == key.lower():
                del self._objects[i]
                return True
        return False

    def clear(self):
        '''removes all sub objects'''
        for item in self._objects:
            if isinstance(item, ConfigListBase):
                item.clear()
                continue
            if isinstance(item, ConfigObjBase):
                del item
                continue
            print("error with", self.var_name, "clear Func")
        del self._objects


    @property
    def count(self) -> int:
        '''returns the count of the config objects'''
        return len(self._objects)


    @property
    def is_section(self) -> bool:
        '''returns if the list is a section'''
        return self.__is_section


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
