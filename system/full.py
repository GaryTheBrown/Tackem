'''Tackem System Full Class'''
from system.base import TackemSystemBase


class TackemSystemFull(TackemSystemBase):
    '''Tackem System Full Class'''

    @property
    def config(self):
        '''grabs the full config'''
        return self._base_data.config


    def set_config(self, location_list: str, value, temp_config=None) -> bool:
        '''recursive method to set a config item'''
        if temp_config is None:
            temp_config = self._base_data.config
        if location_list[0] in temp_config:
            if len(location_list) > 1:
                return self.set_config(location_list[1:], value, temp_config[location_list[0]])
            temp_config[location_list[0]] = value
            return True
        return False

    @property
    def systems(self):
        ''' grabs all systems'''
        return self._base_data.systems


    def system(self, system_name: str):
        ''' grabs a system'''
        return self._base_data.systems.get(system_name, None)

    @property
    def plugins(self):
        '''return all plugins'''
        return self._base_data.plugins


    def plugin(self, plugin_type: str, plugin_name: str):
        '''return a plugin'''
        return self._base_data.plugins.get(plugin_type, {}).get(plugin_name, None)
