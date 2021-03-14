'''Master Section for the Drive controller'''
from libs.database.where import Where
from data.database.ripper import VIDEO_INFO_DB
from libs.database.messages.update import SQLUpdate
from libs.database import Database
from libs.ripper.subsystems import FileSubsystem
from libs.file import File
import os
from data.config import CONFIG
from threading import BoundedSemaphore, Thread
import time
from data.config import CONFIG
from libs.file import File
from libs.ripper.makemkv import MakeMKV


class ISORipper(FileSubsystem):
    '''Master Section for the Drive controller'''

    def __init__(self, pool_sema: BoundedSemaphore, filename: str, video: bool = True):
        super().__init__()
        self._thread = Thread(target=self.__run, args=())
        self._thread.setName(f"Ripper ISO: {filename}")

        self._pool_sema = pool_sema
        self.__filename = filename
        self.__video = video

        self._ripper = None  # whatever the ripper is makemkv and cd ripper
        self.__active = False
        self.__thread_run = True
        self._thread.start()

    @property
    def thread_run(self) -> bool:
        '''return if thread is running'''
        return self._thread.is_alive()

    @property
    def active(self) -> bool:
        '''return if thread is Active'''
        return self.__active

    def stop_thread(self):
        '''stop the thread'''
        if self._thread.is_alive():
            self.__thread_run = False
            self._thread.join()

    def __run(self):
        ''' Loops through the standard ripper function'''
        with self._pool_sema:
            self.__active = True
            if self.__wait_for_file_copy_complete() is False:
                return

            self._get_udfInfo(
                File.location(
                    self.__filename,
                    CONFIG['ripper']['locations']["videoiso" if self.__video else "audioiso"].value
                )
            )
            if self.__thread_run is False:
                return

            if self.__video:
                self._add_video_disc_to_database(self.__filename)
                self._ripper = MakeMKV()
            else:
                return
                # self._ripper = AudioCDLinux(self.get_device(), self._thread.getName(),
                # self._set_drive_status, self._thread_run)
            if self.__thread_run is False:
                return

            self._ripper.call(self._db_id)
            self._ripper = None
            Database.call(
                SQLUpdate(VIDEO_INFO_DB, Where("id", self._db_id), iso_file="")
            )

    def __wait_for_file_copy_complete(self) -> bool:
        '''watches the file size until it stops'''
        path = CONFIG['ripper']["locations"]["videoiso" if self.__video else "audioiso"].value
        filename = File.location(f"{path}{self.__filename}")
        historicalSize = -1
        while (historicalSize != os.path.getsize(filename)):
            if self.__thread_run is False:
                return False
            historicalSize = os.path.getsize(filename)
            time.sleep(4)
        return True

    def api_data(self):
        '''returns the data as json or dict for html'''
        i = f"ripping {self._disc['type']} video disc" if self._ripper else "Waiting For Free Slot"
        return_dict = {
            "filename": self.__filename,
            "info": i,
        }
        if self._ripper:
            return_dict.update(self._ripper.get_ripping_data())
        return return_dict
