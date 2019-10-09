'''Plugin Control Of System Data'''
from system.base import TackemSystemBase


class TackemSystemPlugin(TackemSystemBase):
    '''Plugin Control Of System Data'''


    def __init__(self, plugin_type, plugin_name, instance=None):
        self.__plugin_type = plugin_type
        self.__plugin_name = plugin_name
        self.__plugin_full_name = plugin_type + " " + plugin_name
        self.__plugin_instance = instance
        if isinstance(self.__plugin_instance, str):
            self.__plugin_full_name += " " + instance

        self.__p_config = None
        self.__p_plugin = None
        self.__p_system = None

        _, temp_config = self.get_config(['plugins', self.__plugin_type, self.__plugin_name], {})
        with self._base_data.config_lock:
            if self.__plugin_instance:
                self.__p_config = temp_config[self.__plugin_instance]
            else:
                self.__p_config = temp_config

        with self._base_data.plugins_lock:
            self.__p_plugin = self._base_data.plugins[self.__plugin_type][self.__plugin_name]

        with self._base_data.systems_lock:
            self.__p_system = self._base_data.systems[self.__plugin_full_name]


    @property
    def config(self):
        '''return plugins config'''
        return self.__p_config


    @property
    def plugin(self):
        '''return plugin'''
        return self.__p_plugin


    @property
    def system(self):
        '''return plugins system'''
        return self.__p_system


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
