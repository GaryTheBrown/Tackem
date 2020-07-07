'''Plugin Control Of System Data'''
from system.base import TackemSystemBase

class TackemSystemRoot(TackemSystemBase):
    '''Plugin Control Of System Data'''

    def __init__(self, system_name: str):
        self._system_name = system_name
