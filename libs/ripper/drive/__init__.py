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

    @property
    def device(self) -> str:
        '''returns device READ ONLY SO THREAD SAFE'''
        return self._device

    @property
    def name(self) -> str:
        '''returns the name'''
        name = self._config['label'].value
        device = self._config['link'].value
        return f"{name} ({device})" if name != "" else device

    @property
    def thread_run(self) -> bool:
        '''return if thread is running'''
        return self._thread.is_alive()

    @property
    def drive_status(self) -> str:
        '''returns the drive_status'''
        with self._drive_status_lock:
            drive_status = self._drive_status
        return drive_status

    @drive_status.setter
    def drive_status(self, drive_status: str):
        '''sets the drive_status'''
        with self._drive_status_lock:
            self._drive_status = drive_status

    @property
    def tray_status(self) -> str:
        '''returns the tray_status'''
        with self._tray_status_lock:
            tray_status = self._tray_status
        return tray_status

    @tray_status.setter
    def tray_status(self, tray_status: str):
        '''sets the tray_status'''
        with self._tray_status_lock:
            self._tray_status = tray_status

    @property
    def tray_locked(self) -> bool:
        '''returns the tray_locked'''
        with self._tray_locked_lock:
            tray_locked = self._tray_locked
        return tray_locked

    @tray_locked.setter
    def tray_locked(self, tray_locked: bool):
        '''sets the tray_locked'''
        with self._tray_locked_lock:
            self._tray_locked = tray_locked

    @property
    def disc_type(self) -> str:
        '''returns the disc_type'''
        with self._disc_type_lock:
            disc_type = self._disc_type
        return disc_type

    @disc_type.setter
    def disc_type(self, disc_type: str):
        '''sets the disc_type'''
        with self._disc_type_lock:
            self._disc_type = disc_type

    @property
    def disc_uuid(self) -> str:
        '''returns the disc_uuid'''
        with self._disc_uuid_lock:
            disc_uuid = self._disc_uuid
        return disc_uuid

    @disc_uuid.setter
    def disc_uuid(self, disc_uuid: str):
        '''sets the disc_uuid'''
        with self._disc_uuid_lock:
            self._disc_uuid = disc_uuid

    @property
    def disc_label(self) -> str:
        '''returns the disc_label'''
        with self._disc_label_lock:
            disc_label = self._disc_label
        return disc_label

    @disc_label.setter
    def disc_label(self, disc_label: str):
        '''sets the disc_label'''
        with self._disc_label_lock:
            self._disc_label = disc_label

    @property
    def disc_sha256(self) -> str:
        '''returns the disc_sha256'''
        with self._disc_sha256_lock:
            disc_sha256 = self._disc_sha256
        return disc_sha256

    @disc_sha256.setter
    def disc_sha256(self, disc_sha256: str):
        '''sets the disc_sha256'''
        with self._disc_sha256_lock:
            self._disc_sha256 = disc_sha256

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
            self.drive_status = "checking disc type"
            if self._check_disc_type():
                with self._drive_lock:
                    if not self._thread_run:
                        self.unlock_tray()
                        return
                    if self.disc_type == "audiocd":
                        self.drive_status = "ripping audio cd disc"
                        self._audio_rip()
                    elif self.disc_type == "bluray" or self.disc_type == "dvd":
                        self._check_disc_information()
                        self._drive_status = "ripping video disc"
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
        if self.tray_status == "empty":
            return_dict["traystatus"] = image_folder + "empty.png"
        elif self.tray_status == "open":
            return_dict["traystatus"] = image_folder + "open.png"
        elif self.tray_status == "reading":
            return_dict["traystatus"] = image_folder + "reading.gif"
        elif self.tray_status == "loaded":
            if self.disc_type == "none":
                return_dict["traystatus"] = image_folder + "reading.gif"
            elif self.disc_type == "audiocd":
                return_dict["traystatus"] = image_folder + "audiocd.png"
            elif self.disc_type == "dvd":
                return_dict["traystatus"] = image_folder + "dvd.png"
            elif self.disc_type == "bluray":
                return_dict["traystatus"] = image_folder + "bluray.png"
        return_dict["drivestatus"] = self.drive_status
        return_dict["traylock"] = self.tray_locked
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
