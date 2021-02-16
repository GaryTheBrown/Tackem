'''Master Section for the Drive controller'''
from abc import ABCMeta, abstractmethod
from libs.html_system import HTMLSystem
from data.config import CONFIG
from libs.config.list import ConfigList
import threading
import time
import json

class Drive(metaclass=ABCMeta):
    '''Master Section for the Drive controller'''

    def __init__(self, config: ConfigList):
        self._config = config
        self._device = config['link'].value

        self._thread = threading.Thread(target=self.run, args=())
        self._thread.setName("Ripper Drive:" + self._device)

        self._thread_run = True
        self._drive_lock = threading.Lock()
        self._drive_status = "idle"
        self._drive_status_lock = threading.Lock()
        self._tray_status = "startup"
        self._tray_status_lock = threading.Lock()
        self._tray_locked = False
        self._tray_locked_lock = threading.Lock()
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
    def _set_drive_status(self, drive_status: str):
        '''Threadded Safe Set drive open'''
        with self._drive_status_lock:
            self._drive_status = drive_status

    def _set_tray_status(self, tray_status: str):
        '''Threadded Safe Set tray open'''
        with self._tray_status_lock:
            self._tray_status = tray_status

    def _set_tray_locked(self, tray_locked: bool):
        '''Threadded Safe Set tray locked'''
        with self._tray_locked_lock:
            self._tray_locked = bool(tray_locked)

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
    def get_device(self) -> str:
        '''returns device READ ONLY SO THREAD SAFE'''
        return self._device

    def get_name(self) -> str:
        '''returns the name'''
        name = self._config['label'].value
        device = self._config['link'].value
        return f"{name} ({device})" if name != "" else device

    def get_thread_run(self) -> bool:
        '''return if thread is running'''
        return self._thread.is_alive()

    def get_drive_status(self) -> str:
        '''returns if the drive is open'''
        with self._drive_status_lock:
            drive_status = self._drive_status
        return drive_status

    def get_tray_status(self) -> str:
        '''returns if the tray is open'''
        with self._tray_status_lock:
            tray_status = self._tray_status
        return tray_status

    def get_tray_locked(self) -> bool:
        '''returns if the tray is locked'''
        with self._tray_locked_lock:
            tray_locked = self._tray_locked
        return tray_locked

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
##CHECKS##
##########
    @abstractmethod
    def check_tray(self):
        '''check the status of the disc tray'''

    @abstractmethod
    def _check_disc_type(self, sleep_time=1.0):
        '''Will return the size of the disc'''

    @abstractmethod
    def _check_disc_information(self):
        '''Will return if disc is in drive (setting the UUID and label) or it will return False'''

################
##TRAYCONTROLS##
################

    @abstractmethod
    def open_tray(self):
        '''Send Command to open the tray'''

    @abstractmethod
    def close_tray(self):
        '''Send Command to close the tray'''

    @abstractmethod
    def lock_tray(self):
        '''Send Command to lock the tray'''

    @abstractmethod
    def unlock_tray(self):
        '''Send Command to unlock the tray'''

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

#######
#WAITS#
#######
    def _wait_for_disc(self, sleep_time=1.0, timeout=10):
        '''waits for the disc info to be found'''
        count = 0
        while self.get_tray_status() != "loaded":
            if count >= timeout:
                return False
            if not self._thread_run:
                return False
            time.sleep(float(sleep_time))
            count += 1
            self.check_tray()
        return True

##########
##Script##
##########
    def run(self):
        ''' Loops through the standard ripper function'''
        while self._thread_run:
            self.check_tray()
            while not self._wait_for_disc(timeout=15):
                if not self._thread_run:
                    return
            self.lock_tray()
            self._set_drive_status("checking disc type")
            if self._check_disc_type():
                with self._drive_lock:
                    if not self._thread_run:
                        self.unlock_tray()
                        return
                    if self.get_disc_type() == "audiocd":
                        self._set_drive_status("ripping audio cd disc")
                        self._audio_rip()
                    elif self.get_disc_type() == "bluray" or self.get_disc_type() == "dvd":
                        self._check_disc_information()
                        self._set_drive_status("ripping video disc")
                        self._video_rip()
                    self._ripper.run()
                    self._ripper = None
                if not self._thread_run:
                    self.unlock_tray()
                    return
                self.open_tray()
                self.check_tray()
            self.unlock_tray()
            if not self._thread_run:
                return

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
        tray_status = self.get_tray_status()
        if tray_status == "empty":
            return_dict["traystatus"] = image_folder + "empty.png"
        elif tray_status == "open":
            return_dict["traystatus"] = image_folder + "open.png"
        elif tray_status == "reading":
            return_dict["traystatus"] = image_folder + "reading.gif"
        elif tray_status == "loaded":
            disc_type = self.get_disc_type()
            if disc_type == "none":
                return_dict["traystatus"] = image_folder + "reading.gif"
            elif disc_type == "audiocd":
                return_dict["traystatus"] = image_folder + "audiocd.png"
            elif disc_type == "dvd":
                return_dict["traystatus"] = image_folder + "dvd.png"
            elif disc_type == "bluray":
                return_dict["traystatus"] = image_folder + "bluray.png"
        return_dict["drivestatus"] = self.get_drive_status()
        return_dict["traylock"] = self.get_tray_locked()
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
