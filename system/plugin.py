'''Plugin Control Of System Data'''
from typing import Union
from system.base import TackemSystemBase

class TackemSystemPlugin(TackemSystemBase):
    '''Plugin Control Of System Data'''

    def __init__(self, plugin_type: str, plugin_name: str, instance: Union[str, None] = None):
        self.__plugin_type = plugin_type
        self.__plugin_name = plugin_name
        self.__plugin_full_name = plugin_type + " " + plugin_name
        self.__plugin_instance = instance
        if isinstance(self.__plugin_instance, str):
            self.__plugin_full_name += " " + instance

        self.__p_plugin = self._base_data.plugins[self.__plugin_type][self.__plugin_name]

    @property
    def plugin(self):
        '''return plugin'''
        return self.__p_plugin

    @property
    def plugin_type(self):
        '''returns plugin type'''
        return self.__plugin_type

    @property
    def plugin_name(self):
        '''returns plugin name'''
        return self.__plugin_name

    @property
    def plugin_instance(self):
        '''returns plugin instance name'''
        return self.__plugin_instance

    @property
    def plugin_full_name(self):
        '''returns plugin instance name'''
        return self.__plugin_full_name
