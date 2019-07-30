'''Plugin Control Of System Data'''
from system.base import TackemSystemBase

class TackemSystemRoot(TackemSystemBase):
    '''Plugin Control Of System Data'''
    def __init__(self, system_name):
        self._system_name = system_name
        self._r_config = self._base_data.config[self._system_name]

    def config(self):
        '''return root system config'''
        return self._r_config
