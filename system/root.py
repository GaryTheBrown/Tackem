'''Plugin Control Of System Data'''
from system.base import TackemSystemBase


class TackemSystemRoot(TackemSystemBase):
    '''Plugin Control Of System Data'''


    def __init__(self, system_name: str):
        self._system_name = system_name
        _, self._r_config = self.get_config([self._system_name], {})

    @property
    def config(self):
        '''return root system config'''
        return self._r_config
