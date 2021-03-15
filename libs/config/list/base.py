"""CONFIG List Class"""
import copy
from typing import Any
from typing import Optional

from libs.config.base import ConfigBase
from libs.config.obj.base import ConfigObjBase
from libs.config.rules import ConfigRules


class ConfigListBase(ConfigBase):
    """CONFIG List Class"""

    def __init__(
        self,
        var_name: str,
        label: str,
        *objects,
        help_text: str = "",
        rules: Optional[ConfigRules] = None,
        is_section: bool = False,
        many_section=None,
        many_section_limit_list: Optional[list] = None,
        hide_on_html: bool = False,
        not_in_config: bool = False,
    ):
        super().__init__(var_name, label, help_text, hide_on_html, not_in_config, rules)
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
            self._objects = list(objects)
        else:
            self._objects = []

        if many_section and not isinstance(many_section, ConfigListBase):
            raise ValueError("Many Section is not a config List object or None")
        self.__many_section = many_section
        if many_section_limit_list:
            if not isinstance(many_section_limit_list, list):
                raise ValueError("Many Section Limit List is not a list")
            if all(not isinstance(x, str) for x in many_section_limit_list):
                raise ValueError("All Items in the Many Section Limit List need to be strings")
        self.__many_section_limit_list = many_section_limit_list

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

    def keys(self) -> list:
        """returns all keys for the objects"""
        return [x.var_name for x in self._objects]

    def get(self, key, default: Any = None) -> Any:
        """returns the data if found otherwise returns the default value"""
        for obj in self._objects:
            if obj.key == key.lower():
                return obj
        return default

    def append(self, obj):
        """appends the object to the list"""
        if obj is None:
            return
        if not isinstance(obj, ConfigListBase) and not isinstance(obj, ConfigObjBase):
            raise ValueError("object is not a config object")
        self._objects.append(obj)

    def delete(self, key: str) -> bool:
        """removed the config object according to var_name"""
        for i, obj in enumerate(self._objects):
            if obj.key == key.lower():
                del self._objects[i]
                return True
        return False

    def clear(self):
        """removes all sub objects"""
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
        """returns the count of the config objects"""
        return len(self._objects)

    @property
    def is_section(self) -> bool:
        """returns if the list is a section"""
        return self.__is_section

    @property
    def many_section(self):
        """returns the Many Section"""
        return self.__many_section

    @property
    def many_section_limit_list(self) -> list:
        """returns the Many Section Limit List"""
        return self.__many_section_limit_list

    def clone_many_section(self, var_name: str) -> bool:
        """Clones the Many Section For Multi Instance config sections"""
        var = var_name.lower().replace(" ", "")
        if var in self.keys():
            return False
        if self.many_section:
            new = copy.deepcopy(self.__many_section)
            new.label = var_name.capitalize()
            new.var_name = var
            self.append(new)
            return True
        return False

    def find_and_get(self, location: list) -> Any:
        """Find and Get a config Item"""
        for obj in self._objects:
            if location[0] != obj.var_name:
                continue
            if isinstance(obj, ConfigObjBase):
                if len(location) == 1:
                    return obj.value
                return None
            if isinstance(obj, ConfigListBase):
                if len(location) > 1:
                    return obj.find_and_get(location[1:])
                return None

        for obj in self._objects:
            if isinstance(obj, ConfigListBase) and obj.is_section:
                if location[0] in obj:
                    return obj.find_and_get(location)
        return None

    def find_and_set(self, location: list, value: Any):
        """Find and set a config Item"""
        for obj in self._objects:
            if location[0] != obj.var_name:
                continue
            if isinstance(obj, ConfigObjBase):
                if len(location) == 1:
                    obj.value = value
                    return
            if isinstance(obj, ConfigListBase):
                if len(location) > 1:
                    obj.find_and_set(location[1:], value)
                    return
            return

        for obj in self._objects:
            if isinstance(obj, ConfigListBase) and obj.is_section:
                if location[0] in obj:
                    obj.find_and_set(location, value)
                    return
        return
