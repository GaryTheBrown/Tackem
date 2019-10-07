'''Plugin Control Of System Data'''
from system.base import TackemSystemBase


class TackemSystemPlugin(TackemSystemBase):
    '''Plugin Control Of System Data'''


    def __init__(self, plugin_type, plugin_name, instance=None):
        self._plugin_type = plugin_type
        self._plugin_name = plugin_name
        self._name = plugin_type + " " + plugin_name
        self._instance = instance
        if isinstance(self._instance, str):
            self._name += " " + instance

        self._p_config = None
        self._p_plugin = None
        # self._p_system = None
        _, temp_config = self.get_config(['plugins', self._plugin_type, self._plugin_name], {})
        with self._base_data.config_lock:
            if self._instance:
                self._p_config = temp_config[self._instance]
            else:
                self._p_config = temp_config

        with self._base_data.plugins_lock:
            self._p_plugin = self._base_data.plugins[self._plugin_type][self._plugin_name]

        # with self._base_data.systems_lock:
        #     self._p_system = self._base_data.systems[self._name]


    def config(self):
        '''return plugins config'''
        return self._p_config


    def plugin(self):
        '''return plugin'''
        return self._p_plugin


    # def system(self):
    #     '''return plugins system'''
    #     return self._p_system
