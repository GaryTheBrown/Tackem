'''Config List Class'''
from configobj import ConfigObj
from validate import Validator
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.config.configobj_extras import EXTRA_FUNCTIONS
from libs.config.list.base import ConfigListBase
from libs.config.obj.base import ConfigObjBase


class ConfigListFile(ConfigListBase):
    '''Config List Class'''

    __config = None

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
            self.__config.write()
        except OSError:
            print("ERROR WRITING CONFIG FILE")


    def update_configobj(self, config=None):
        '''Updates the config Object for saving'''
        if self._objects is None:
            return

        if config is None:
            config = self.__config


        for item in self._objects:
            if isinstance(item, ConfigListBase):
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
        if self._objects is None:
            return

        if config is None:
            config = self.__config

        for item in self._objects:
            if isinstance(item, ConfigListBase):
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

        if self.many_section:
            return_string += self.__tab(indent) + self.__open_bracket(indent + 1)
            return_string += "__many__" + self.__close_bracket(indent + 1) + "\n"
            return_string += self.many_section.get_spec_part(indent + 1)
        else:
            for item in self._objects:
                if item.not_in_config:
                    continue
                if isinstance(item, ConfigListBase):
                    if item.is_section:
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
