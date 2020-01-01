'''Tackem System Full Class'''
from system.base import TackemSystemBase


class TackemSystemFull(TackemSystemBase):
    '''Tackem System Full Class'''


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
