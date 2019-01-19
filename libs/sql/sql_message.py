'''SQL MESSAGE SYSTEM DATA'''
import threading

class SQLMessage:
    '''Struct to hold the message for easier reading in here'''
    def __init__(self, system_name, special_command=None, command=None, table_name=None,
                 return_data=None, data=None, version=None, return_dict=True):
        self._lock = threading.Lock()
        self._event_lock = threading.Event()
        #INPUTS
        self._system_name = system_name
        self._special_command = special_command
        self._command = command
        self._table_name = table_name
        self._return_data = return_data
        self._data = data
        self._version = version
        self._return_dict = return_dict
        #OUTPUTS
        self._return_data = return_data #area to store any data to return from the data class

    def __repr__(self):
        '''print return'''
        return_string = "SQLMessage(" + self._system_name + ", " + self._special_command + ")\n"
        return_string += "\t" + str(self._command) + ", " + str(self._table_name)
        return_string += ", " + str(self._version)
        return return_string

    def system_name(self):
        '''Return system Name'''
        with self._lock:
            return self._system_name
    def special_command(self):
        '''Return special command'''
        with self._lock:
            return self._special_command
    def command(self):
        '''Return command'''
        with self._lock:
            return self._command
    def table_name(self):
        '''Return table_name'''
        with self._lock:
            return self._table_name
    def data(self):
        '''Return data'''
        with self._lock:
            return self._data
    def version(self):
        '''Return version'''
        with self._lock:
            return self._version

    def return_dict(self):
        '''Return if return should be dict'''
        with self._lock:
            return self._return_dict

    def return_data(self):
        '''Return return data'''
        with self._lock:
            return self._return_data

    def set_return_data(self, data):
        '''Sets Return Data'''
        with self._lock:
            self._return_data = data

    def event_wait(self):
        '''makes system wait for event to be issued'''
        self._event_lock.wait()

    def event_set(self):
        '''sets the event for the other thread to resume'''
        self._event_lock.set()
