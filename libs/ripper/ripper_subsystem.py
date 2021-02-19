'''shared info between video ripper and audio cd ripper'''
from typing import Callable

class RipperSubSystem():
    '''Subsystem controller'''

    def __init__(self, device: str, thread_name: str, thread_run: bool):
        self._device = device
        self._thread_name = thread_name
        self._thread_run = thread_run

        self._ripping_track = None
        self._ripping_file = 0
        self._ripping_total = 0
        self._ripping_max = 0
        self._ripping_file_p = 0.0
        self._ripping_total_p = 0.0

###########
##GETTERS##
###########
    def get_ripping_data(self) -> dict:
        '''returns the data as dict for html'''
        return {
            'track': self._ripping_track,
            'file': self._ripping_file,
            'total': self._ripping_total,
            'max': self._ripping_max,
            'file_percent': self._ripping_file_p,
            'total_percent': self._ripping_total_p
        }
