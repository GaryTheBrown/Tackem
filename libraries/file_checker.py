'''
Creates checksum hash for a file in Binary from SHA256
If storing in the DB you need a BINARY(32)
'''
import datetime
import hashlib
import threading
from pathlib import Path
from data.config import CONFIG
from libs.database import Database
from libs.database.messages import SQLSelect, SQLUpdate
from libs.database.where import Where
from data.database.library import LIBRARY_FILES_DB

class FileChecker:
    '''system to check the files are not damaged'''

    __BLOCKSIZE = 65536
    __list = []
    __event = threading.Event()
    __lock = threading.Lock()
    __config = CONFIG['libraries']['global']['autofilecheck']

    def __init__(self):

        self.__thread_name = "Library File Checker"
        self.__thread = threading.Thread(target=self.run, args=())
        self.__thread.setName(self.__thread_name)

        self._thread_run = False

    def start(self):
        '''starts the file checker'''
        if self._thread_run is False:
            self._thread_run = True
            self.__thread.start()

    def stop(self):
        '''stops the Library'''
        if self._thread_run is True:
            self._thread_run = False
            self.__event.set()

    def extend(self, data: list):
        '''Extend the list of files to check'''
        with self.__lock:
            self.__list.extend(data)
        self.__event.set()

    def get_file_checksum(self, file: str) -> str:
        '''Creates checksum hash for a file in Binary from SHA256'''

        hasher = hashlib.sha256()
        with open(file, 'rb') as open_file:
            buffer = open_file.read(self.__BLOCKSIZE)
            while len(buffer) > 0:
                hasher.update(buffer)
                buffer = open_file.read(self.__BLOCKSIZE)
        return hasher.digest()

    def check_for_files(self):
        '''Threadded Script For running'''
        regularity = self.__config['regularity'].value

        if regularity == "disabled":
            return

        now = datetime.datetime.now()
        if regularity == "hourly":
            now = now + datetime.timedelta(hours=-1)
        if regularity == "daily":
            now = now + datetime.timedelta(days=-1)
        if regularity == "weekly":
            now = now + datetime.timedelta(weeks=-1)
        if regularity == "monthly":
            now = now + datetime.timedelta(months=-1)
        if regularity == "quaterly":
            now = now + datetime.timedelta(months=-3)
        if regularity == "halfyear":
            now = now + datetime.timedelta(months=-6)
        if regularity == "year":
            now = now + datetime.timedelta(years=-1)

        timestamp = int(now.timestamp())
        msg = SQLSelect(
            LIBRARY_FILES_DB.name(),
            Where("last_check", timestamp, ">")
        )

        Database.call(msg)

        self.extend(msg.return_data)

    def run(self):
        '''Threadded Script For running'''
        while self._thread_run:
            self.__event.wait()
            if not self._thread_run:
                return

            self.__check_list()
            self.__event.clear()
            if not self._thread_run:
                return

    def __check_list(self):
        while self.__list:
            if not self._thread_run:
                return

            with self.__lock:
                item = self.__list.pop()

            full_path = item['folder'] + item['file']
            if Path(full_path).is_file():
                checksum = self.get_file_checksum(full_path)

                update_data = {
                    "checksum": checksum
                }

                if checksum != item['checksum']:
                    print(f"FILE HAS GONE BAD {full_path}")
                    update_data['bad_file'] = 1

                msg = SQLUpdate(
                    LIBRARY_FILES_DB.name(),
                    Where("id", item['id']),
                    checksum=checksum
                )

            else:
                msg = SQLUpdate(
                    LIBRARY_FILES_DB.name(),
                    Where("id", item['id']),
                    missing_file=1
                )

            Database.call(msg)
