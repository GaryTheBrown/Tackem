'''Master Section for the Renamer controller'''
import threading
import time
from .data.events import RipperEvents

class Renamer():
    '''Master Section for the Renamer controller'''
    def __init__(self, config, db):
        self._events = RipperEvents()
        self._config = config
        self._db = db

        self._thread = threading.Thread(target=self.run, args=())
        self._thread.setName("Renamer")
        self._thread_run = True

##########
##Thread##
##########

    def start_thread(self):
        '''start the thread'''
        if not self._thread.is_alive():
            self._thread.start()
            return True
        return False

    def stop_thread(self):
        '''stop the thread'''
        if self._thread.is_alive():
            self._thread_run = False
            self._thread.join()

##########
##Script##
##########
    def run(self):
        ''' Loops through the standard renamer function'''
        while self._thread_run:
            #actions here with bellow code included
            if not self._thread_run:
                return

            #after doing everything needed just sleep till woken up.
            if not self._thread_run:
                return
            self._events.renamer.clear()
            self._events.renamer.wait()
            time.sleep(1.0)
