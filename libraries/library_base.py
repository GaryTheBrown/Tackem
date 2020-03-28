'''Base Library Controller'''
from abc import ABCMeta, abstractmethod
import threadding
from libs.config.list import ConfigList

class LibraryBase(metaclass=ABCMeta):
    '''Base Library Class'''

    def __init__(self, name: str, library_type: str, config: ConfigList):
        self._name = name
        self._library_type = library_type
        self._config = config

        self._thread_run = False


    def stop(self):
        '''stops the Library'''
        if self._thread_run is False:
            self._thread_run = False

    @abstractmethod
    def run(self):
        '''threadded run'''
