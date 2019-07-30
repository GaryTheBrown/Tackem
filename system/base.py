'''Tackem System Data Base Class'''
from system.data import SystemData
class TackemSystemBase:
    '''Tackem System Data Base Class'''
    _base_data = SystemData()

    def get_sql(self):
        '''get sql'''
        return self._base_data.sql

    def get_auth(self):
        '''get auth'''
        return self._base_data.auth

    def get_musicbrainz(self):
        '''get musicbrainz'''
        return self._base_data.musicbrainz

    def get_config(self, location_list, default, temp_config=None):
        '''recursive method to grab a config item read only'''
        if temp_config is None:
            temp_config = self._base_data.config
        if location_list[0] in temp_config:
            if len(location_list) > 1:
                return self.get_config(location_list[1:], default, temp_config[location_list[0]])
            return temp_config.get(location_list[0], default)
        return default

    def get_baseurl(self):
        '''grab the baseurl'''
        return self.get_config(["webui", "baseurl"], "/")
