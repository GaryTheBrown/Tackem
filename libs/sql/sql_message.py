'''SQL MESSAGE SYSTEM DATA'''
from typing import Optional, Union
import threading


class SQLMessage:
    '''Struct to hold the message for easier reading in here'''

    def __init__(
            self,
            system_name: str,
            special_command: Optional[str] = None,
            command: Optional[str] = None,
            table_name: Optional[str] = None,
            return_data: Optional[list] = None,
            data: Optional[list] = None,
            version: Union[int, str] = None,
            return_dict: bool = True
    ):
        self._lock = threading.Lock()
        self._event_lock = threading.Event()
        # INPUTS
        self._system_name = system_name
        self._special_command = special_command
        self._command = command
        self._table_name = table_name
        self._return_data = return_data
        self._data = data
        self._version = version
        self._return_dict = return_dict
        # OUTPUTS
        # area to store any data to return from the data class
        self._return_data = return_data

    def __repr__(self) -> str:
        '''print return'''
        return_string = "SQLMessage(" + self._system_name + \
            ", " + self._special_command + ")\n"
        return_string += "\t" + str(self._command) + \
            ", " + str(self._table_name)
        return_string += ", " + str(self._version)
        return return_string

    @property
    def system_name(self) -> str:
        '''Return system Name'''
        with self._lock:
            return self._system_name

    @property
    def special_command(self) -> Optional[str]:
        '''Return special command'''
        with self._lock:
            return self._special_command

    @property
    def command(self) -> str:
        '''Return command'''
        with self._lock:
            return self._command

    @property
    def table_name(self) -> str:
        '''Return table_name'''
        with self._lock:
            return self._table_name

    @property
    def data(self) -> list:
        '''Return data'''
        with self._lock:
            return self._data

    @property
    def version(self) -> int:
        '''Return version'''
        with self._lock:
            return self._version

    @property
    def return_dict(self) -> bool:
        '''Return if return should be dict'''
        with self._lock:
            return self._return_dict

    @property
    def return_data(self) -> list:
        '''Return return data'''
        with self._lock:
            return self._return_data

    def set_return_data(self, data: list):
        '''Sets Return Data'''
        with self._lock:
            self._return_data = data

    def event_wait(self):
        '''makes system wait for event to be issued'''
        self._event_lock.wait()

    def event_set(self):
        '''sets the event for the other thread to resume'''
        self._event_lock.set()
