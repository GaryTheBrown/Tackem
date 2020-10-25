'''SQL MESSAGE SYSTEM DATA'''
from typing import Union
import threading
from libs.database.table import Table

class SQLMessage:
    '''Struct to hold the message for easier reading in here'''

    def __init__(
            self,
            query: Union[str, Table]
    ):
        self.__lock = threading.Lock()
        self.__event_lock = threading.Event()
        # INPUTS
        self.__thread_ident = threading.get_ident()
        self.__query = query
        self.__return_data = []

        print(query)

    @property
    def query(self) -> str:
        '''Return query'''
        with self.__lock:
            return self.__query

    @property
    def return_data(self) -> list:
        '''Return return data'''
        with self.__lock:
            return self.__return_data

    @return_data.setter
    def return_data(self, data: list):
        '''Sets Return Data'''
        with self.__lock:
            self.__return_data = data

    def event_wait(self):
        '''makes system wait for event to be issued'''
        self.__event_lock.wait()

    def event_set(self):
        '''sets the event for the other thread to resume'''
        self.__event_lock.set()
