'''Tackem System Full Class'''
from system.base import TackemSystemBase
class TackemSystemFull(TackemSystemBase):
    '''Tackem System Full Class'''

    def config(self):
        '''grabs the full config'''
        return self._base_data.config

    def set_config(self, location_list, value, temp_config=None):
        '''recursive method to grab a config item read only'''
        if temp_config is None:
            temp_config = self._base_data.config
        if location_list[0] in temp_config:
            if len(location_list) > 1:
                return self.get_config(location_list[1:], value, temp_config[location_list[0]])
            return temp_config.set(location_list[0], value)
        return False

    def systems(self):
        ''' grabs all systems'''
        return self._base_data.systems

    def system(self, system_name):
        ''' grabs a system'''
        return self._base_data.systems.get(system_name, None)

    def plugins(self):
        '''return all plugins'''
        return self._base_data.plugins

    def plugin(self, plugin_type, plugin_name):
        '''return a plugin'''
        return self._base_data.plugins.get(plugin_type, {}).get(plugin_name, None)
