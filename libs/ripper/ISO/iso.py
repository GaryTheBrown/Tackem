'''Master Section for the Drive controller'''
from abc import ABCMeta, abstractmethod
from libs.html_system import HTMLSystem
from data.config import CONFIG
from libs.config.list import ConfigList
import threading
import time
import json

class ISORipper(metaclass=ABCMeta):
    '''Master Section for the Drive controller'''

    def __init__(self, iso_file: str, type: str, uuid: str, label: str, sha256: str):
        self._config = config
        self._device = config['link'].value

        self._thread = threading.Thread(target=self.run, args=())
        self._thread.setName("Ripper ISO:" + self._device)

        self._thread_run = True
        self._disc_type = "none"
        self._disc_type_lock = threading.Lock()
        self._disc_uuid = None
        self._disc_uuid_lock = threading.Lock()
        self._disc_label = None
        self._disc_label_lock = threading.Lock()
        self._disc_sha256 = None
        self._disc_sha256_lock = threading.Lock()

        self._ripper = None # whatever the ripper is makemkv and cd ripper

###########
##SETTERS##
###########
    def _set_disc_type(self, disc_type: str):
        '''Threadded Safe Set disc type'''
        with self._disc_type_lock:
            self._disc_type = disc_type

    def _set_disc_uuid(self, disc_uuid: str):
        '''Threadded Safe Set disc uuid'''
        with self._disc_uuid_lock:
            self._disc_uuid = disc_uuid

    def _set_disc_label(self, disc_label: str):
        '''Threadded Safe Set disc label'''
        with self._disc_label_lock:
            self._disc_label = disc_label

    def _set_disc_sha256(self, disc_sha256: str):
        '''Threadded Safe Set disc sha256'''
        with self._disc_sha256_lock:
            self._disc_sha256 = disc_sha256

###########
##GETTERS##
###########
    def get_thread_run(self) -> bool:
        '''return if thread is running'''
        return self._thread.is_alive()

    def get_disc_type(self) -> str:
        '''returns the disc type if a disc is in the drive'''
        with self._disc_type_lock:
            disc_type = self._disc_type
        return disc_type

    def get_disc_uuid(self) -> str:
        '''returns the disc uuid if a disc is in the drive'''
        with self._disc_uuid_lock:
            disc_uuid = self._disc_uuid
        return disc_uuid

    def get_disc_label(self) -> str:
        '''returns the disc label if a disc is in the drive'''
        with self._disc_label_lock:
            disc_label = self._disc_label
        return disc_label

    def get_disc_sha256(self) -> str:
        '''returns the disc sha256 if a disc is in the drive'''
        with self._disc_sha256_lock:
            disc_sha256 = self._disc_sha256
        return disc_sha256

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
        disc_type = self.get_disc_type()
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
