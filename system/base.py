'''Tackem System Data Base Class'''
from system.data import SystemData


class TackemSystemBase:
    '''Tackem System Data Base Class'''


    _base_data = SystemData()


    @property
    def sql(self):
        '''get sql'''
        return self._base_data.sql


    @property
    def auth(self):
        '''get auth'''
        return self._base_data.auth


    @property
    def musicbrainz(self):
        '''get musicbrainz'''
        return self._base_data.musicbrainz


    def get_config(self, location_list: list, default, temp_config=None) -> tuple:
        '''recursive method to grab a config item read only'''
        if temp_config is None:
            temp_config = self._base_data.config
        if location_list[0] in temp_config:
            if len(location_list) > 1:
                return self.get_config(location_list[1:], default, temp_config[location_list[0]])
            return True, temp_config.get(location_list[0], default)
        return False, default


    @property
    def baseurl(self):
        '''grab the baseurl'''
        return self.get_config(["webui", "baseurl"], "/")[1]


    def system_keys(self):
        '''returns the system keys for navbar'''
        with self._base_data.systems_lock:
            return self._base_data.systems.keys()
