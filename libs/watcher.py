'''Custom Watchers'''
import time
import os
import threading
from typing import Callable

class FolderWatcher:
    '''Custom Folder Watcher'''

    __single_sleep = 1

    def __init__(self,
        folder: str,
        callable: Callable, # (folder, difference in count since last)
        recursive: bool = True,
        sleep_timer: int = 300
    ):
        self.__folder = folder
        self.__callable = callable
        self.__folder_count = False
        self.__recursive = recursive
        self.__sleep_timer = sleep_timer

        self._thread = threading.Thread(target=self.run, args=())
        self._thread.setName(f"Folder Watcher: {folder}")

    @property
    def thread_run(self) -> bool:
        '''return if thread is running'''
        return self._thread.is_alive()

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

    def run(self):
        '''Folder Watcher Script'''
        while self._thread_run:
            if self.__recursive:
                new_count = len(os.listdir(self.__folder))
            else:
                new_count = len(next(os.walk(self.__folder))[2])
            if not self._thread_run:
                return
            if isinstance(self.__folder_count, int):
                if self.__folder_count != new_count:
                    self.__callable()
            else:
                self.__folder_count = new_count
            if not self._thread_run:
                return
            sleep_timer = 0
            while sleep_timer < self.__sleep_timer:
                time.sleep(self.__single_sleep)
                if not self._thread_run:
                    return
                sleep_timer += self.__single_sleep
