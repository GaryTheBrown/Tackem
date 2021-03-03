'''Master Section for the Drive controller'''
from libs.ripper.subsystems import FileSubsystem
from libs.file import File
import os
from libs.html_system import HTMLSystem
from data.config import CONFIG
from threading import BoundedSemaphore, Thread
import time
import json
from libs.database.where import Where
from data.database.ripper import VIDEO_INFO_DB
from libs.database.messages.update import SQLUpdate
from libs.database import Database
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

        self._ripper = None # whatever the ripper is makemkv and cd ripper
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

##########
##Script##
##########
    def __run(self):
        ''' Loops through the standard ripper function'''
        with self._pool_sema:
            self.__active = True
            self.__wait_for_file_copy_complete()
            self._get_udfInfo(
                File.location(
                    self.__filename,
                    CONFIG['ripper']['locations']["videoiso" if self.__video else "audioiso"].value
                )
            )

            if self.__video:
                self._add_video_disc_to_database(self.__filename)
                self._ripper = MakeMKV()
            else:
                pass
                # self._ripper = AudioCDLinux(self.get_device(), self._thread.getName(),
                                              # self._set_drive_status, self._thread_run)

            self._ripper.call(self._db_id)
            self._ripper = None

    def __wait_for_file_copy_complete(self) -> bool:
        '''watches the file size until it stops'''
        path = CONFIG['ripper']["locations"]["videoiso" if self.__video else "audioiso"].value
        filename = File.location(f"{path}{self.__filename}")
        historicalSize = -1
        while (historicalSize != os.path.getsize(filename)):
            historicalSize = os.path.getsize(filename)
            time.sleep(4)

##############
##HTML STUFF##
##############
    def api_data(self, return_json=True):
        '''returns the data as json or dict for html'''
        return_dict = {}
        image_folder = CONFIG["webui"]["baseurl"].value + "static/img/"
        disc_type = self.__type
        if disc_type == "audiocd":
            return_dict["traystatus"] = image_folder + "audiocd.png"
        elif disc_type == "dvd":
            return_dict["traystatus"] = image_folder + "dvd.png"
        elif disc_type == "bluray":
            return_dict["traystatus"] = image_folder + "bluray.png"
        if self._ripper:
            ripping_data = self._ripper.get_ripping_data()
            if ripping_data['track'] is not None:
                return_dict["ripping"] = True
                file_percent = "Track " + str(ripping_data['track']) + " ("
                file_percent += str(ripping_data['file_percent']) + "%)"
                total_percent = "Total (" + \
                    str(ripping_data['total_percent']) + "%)"

                return_dict["rippingdata"] = HTMLSystem.part("ripping/drives/rippingdata",
                    PROGRESSTRACK=HTMLSystem.part("other/progress",
                        LABEL=file_percent,
                        VALUE=ripping_data['file'],
                        MAX=ripping_data['max'],
                        PERCENT=ripping_data['file_percent']
                    ),
                    PROGRESSTOTAL=HTMLSystem.part("other/progress",
                        LABEL=total_percent,
                        VALUE=ripping_data['total'],
                        MAX=ripping_data['max'],
                        PERCENT=ripping_data['total_percent']
                    )
                )
            else:
                return_dict["ripping"] = False
        else:
            return_dict["ripping"] = False
        if return_json:
            return json.dumps(return_dict)
        return return_dict
