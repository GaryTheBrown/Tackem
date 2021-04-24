"""Master Section for the Drive controller"""
from threading import BoundedSemaphore
from threading import Thread
from typing import Union

from config import CONFIG
from database.ripper.video_info import RipperVideoInfo
from libs.file import File
from ripper.makemkv import MakeMKV
from ripper.subsystems import FileSubsystem


class ISORipper(FileSubsystem):
    """Master Section for the Drive controller"""

    def __init__(self, pool_sema: BoundedSemaphore, filename: str):
        super().__init__()
        self._thread = Thread(target=self.__run, args=())
        self._thread.setName(f"Ripper ISO: {filename}")

        self._pool_sema = pool_sema
        self.__filename = filename

        self._ripper: Union[MakeMKV] = None  # whatever the ripper is makemkv and cd ripper
        self.__active = False
        self.__thread_run = True
        self._thread.start()

    @property
    def thread_run(self) -> bool:
        """return if thread is running"""
        return self._thread.is_alive()

    @property
    def active(self) -> bool:
        """return if thread is Active"""
        return self.__active

    @property
    def filename(self):
        """returns the filename"""
        return self.__filename

    def stop_thread(self):
        """stop the thread"""
        if self._thread.is_alive():
            self.__thread_run = False
            self._thread.join()

    def __run(self):
        """ Loops through the standard ripper function"""
        with self._pool_sema:
            self.__active = True

            self._get_udfInfo(
                File.location(self.__filename, CONFIG["webui"]["uploadlocation"].value)
            )
            if self.__thread_run is False:
                return

            if self._disc["type"] == "audiocd":
                return
                # self._ripper = AudioCDLinux(self.get_device(), self._thread.getName(),
                # self._set_drive_status, self._thread_run)
            else:
                self._add_video_disc_to_database(self.__filename)
                self._ripper = MakeMKV()
            if self.__thread_run is False:
                return

            self._ripper.call(self._db_id)
            self._ripper = None
            if self._disc["type"] == "audiocd":
                pass
            else:
                RipperVideoInfo.do_update({"iso_file": ""}).where(
                    RipperVideoInfo.id == self._db_id
                ).execute()
            File.rm(File.location(self.__filename, CONFIG["webui"]["uploadlocation"].value))

    def api_data(self):
        """returns the data as json or dict for html"""
        i = f"ripping {self._disc['type']} disc" if self._ripper else "Waiting For Free Slot"
        return_dict = {
            "filename": self.__filename,
            "info": i,
        }
        if self._ripper:
            return_dict.update(self._ripper.get_ripping_data())
        return return_dict

    def html_data(self) -> dict:
        """returns the data for html"""
        return_dict = self.api_data()
        return return_dict
