"""Custom Watchers"""
import os
import threading
import time
from typing import Callable

from libs.file import File


class FolderWatcher:
    """Custom Folder Watcher"""

    __single_sleep = 1

    def __init__(
        self,
        folder: str,
        # (folder, difference in count since last)
        callable: Callable[[], None],
        recursive: bool = True,
        sleep_timer: int = 300,
    ):
        self.__folder = File.location(folder)
        self.__callable = callable
        self.__folder_count = False
        self.__recursive = recursive
        self.__sleep_timer = sleep_timer

        self._thread = threading.Thread(target=self.run, args=())
        self._thread.setName(f"Folder Watcher: {folder}")
        self.__thread_run = True
        self._thread.start()

    def stop_thread(self):
        """stop the thread"""
        if self._thread.is_alive():
            self.__thread_run = False
            self._thread.join()

    def run(self):
        """Folder Watcher Script"""
        while self.__thread_run:
            if self.__recursive:
                new_count = len(os.listdir(self.__folder))
            else:
                new_count = len(next(os.walk(self.__folder))[2])
            if not self.__thread_run:
                return
            if isinstance(self.__folder_count, int):
                if self.__folder_count != new_count:
                    self.__callable()
            else:
                self.__folder_count = new_count
            if not self.__thread_run:
                return
            sleep_timer = 0
            while sleep_timer < self.__sleep_timer:
                time.sleep(self.__single_sleep)
                if not self.__thread_run:
                    return
                sleep_timer += self.__single_sleep
