'''Config List Class'''
from libs.config.base import ConfigBase
# from libs.config.rules import ConfigRules
from libs.config.obj.base import ConfigObjBase

class ConfigList(ConfigBase):
    '''Config List Class'''


    def __init__(
            self,
            name: str,
            label: str,
            help_text: str,
            priority: int,
            *objects,
            hide_on_html: bool = False,
            read_only: bool = False,
            disabled: bool = False,
            rules=None,
        ):
        super().__init__(name, label, help_text, priority, hide_on_html, read_only, disabled, rules)
        self.__objects = []

        for obj in objects:
            if isinstance(obj, (ConfigObjBase, ConfigList)):
                self.__objects.append(obj)


    def __getitem__(self, key):
        if isinstance(key, int):
            return self.__objects[key]
        for obj in self.__objects:
            if obj.name.lower() == key.lower():
                return obj
        return None


    def __iter__(self):
        return iter(self.__objects)


    def __len__(self):
        return len(self.__objects)
