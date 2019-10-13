'''Plugin website Control Of System Data'''
from typing import Union
from system.plugin import TackemSystemPlugin


class TackemSystemWeb(TackemSystemPlugin):
    '''Plugin Control Of System Data'''


    def __init__(self, plugin_type: str, plugin_name: str, instance: Union[str, None] = None):
        super().__init__(plugin_type, plugin_name, instance)
        self._p_system = None
        with self._base_data.systems_lock:
            self._p_system = self._base_data.systems[self._name]

    @property
    def system(self):
        '''return plugins system'''
        with self._base_data.systems_lock:
            return self._p_system
