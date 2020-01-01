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
    def musicbrainz(self):
        '''get musicbrainz'''
        return self._base_data.musicbrainz


    def system_keys(self):
        '''returns the system keys for navbar'''
        return self._base_data.systems.keys()
