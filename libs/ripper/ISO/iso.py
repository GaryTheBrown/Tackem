'''Master Section for the Drive controller'''
from abc import ABCMeta, abstractmethod
from libs.file import File
from libs.database.where import Where
import os
from libs.html_system import HTMLSystem
from data.config import CONFIG
from threading import BoundedSemaphore, Thread
import time
import json

class ISORipper(metaclass=ABCMeta):
    '''Master Section for the Drive controller'''

    def __init__(self, db_data: dict, pool_sema: BoundedSemaphore):
        self._thread = Thread(target=self.run, args=())
        self._thread.setName(f"Ripper ISO: {db_data['iso_file']}")

        self._pool_sema = pool_sema
        self._db_data = db_data

        self._ripper = None # whatever the ripper is makemkv and cd ripper

    @property
    def thread_run(self) -> bool:
        '''return if thread is running'''
        return self._thread.is_alive()

    def wait_for_file_copy_complete(self, audio: bool = False) -> bool:
        '''watches the file size until it stops'''
        path = CONFIG['ripper']["locations"]["audioiso" if audio else "videoiso"].value
        filename = File.location(f"{path}{self._db_data['iso_file']}")
        historicalSize = -1
        while (historicalSize != os.path.getsize(filename)):
            historicalSize = os.path.getsize(filename)
            time.sleep(1)

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
        ''' Loops through the standard ripper function'''
        with self._pool_sema:
            if "uuid" in self._db_data:
                self.wait_for_file_copy_complete()
                self._video_rip()
            else:
                self.wait_for_file_copy_complete(True)
                self._audio_rip()

    @abstractmethod
    def _audio_rip(self):
        '''script to rip an audio cd'''

    @abstractmethod
    def _video_rip(self):
        '''script to rip video disc'''

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
