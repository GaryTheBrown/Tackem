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

    def __init__(self, db_data: dict, pool_sema: BoundedSemaphore):
        self._thread = Thread(target=self.__run, args=())
        self._thread.setName(f"Ripper ISO: {db_data['iso_file']}")

        self._pool_sema = pool_sema
        self._db_data = db_data

        self._ripper = None # whatever the ripper is makemkv and cd ripper
        self.__active = False
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
            self._thread_run = False
            self._thread.join()

##########
##Script##
##########
    def __run(self):
        ''' Loops through the standard ripper function'''
        with self._pool_sema:
            self.__active = True
            if "uuid" in self._db_data:
                self.__wait_for_file_copy_complete()
                file = File.location(
                    self._db_data['iso_file'],
                    CONFIG['ripper']['locations']['videoiso'].value
                )

                disc = self._get_udfInfo(file)

                Database.call(
                    SQLUpdate(
                        VIDEO_INFO_DB,
                        Where("id", self._db_data['id']),
                        label=disc['label'],
                        uuid=disc['uuid'],
                        disc_type=disc['type']
                    )
                )
                self._ripper = MakeMKV("")
            else:
                self.__wait_for_file_copy_complete(True)
                # self._ripper = AudioCDLinux(self.get_device(), self._thread.getName(),
                                              # self._set_drive_status, self._thread_run)

            while self._thread_run:
                time.sleep(1)

            # self._ripper.call(self._db_data['id'])
            self._ripper = None

    def __wait_for_file_copy_complete(self, audio: bool = False) -> bool:
        '''watches the file size until it stops'''
        path = CONFIG['ripper']["locations"]["audioiso" if audio else "videoiso"].value
        filename = File.location(f"{path}{self._db_data['iso_file']}")
        historicalSize = -1
        while (historicalSize != os.path.getsize(filename)):
            historicalSize = os.path.getsize(filename)
            time.sleep(1)

##############
##HTML STUFF##
##############
    def html_data(self, return_json=True):
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
