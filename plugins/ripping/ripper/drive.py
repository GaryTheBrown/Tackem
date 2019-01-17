'''Master Section for the Drive controller'''
from abc import ABCMeta, abstractmethod
import threading
import time

class Drive(metaclass=ABCMeta):
    '''Master Section for the Drive controller'''
    def __init__(self, cfg_name, device_info, config, db):
        self._cfg_name = cfg_name
        self._device_info = device_info
        self._device = device_info['link']
        self._config = config
        self._db = db

        self._thread = threading.Thread(target=self.run, args=())
        self._thread.setName("Ripper:" + self._device)

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

###########
##SETTERS##
###########
    def _set_drive_status(self, drive_status):
        '''Threadded Safe Set drive open'''
        with self._drive_status_lock:
            self._drive_status = drive_status

    def _set_tray_status(self, tray_status):
        '''Threadded Safe Set tray open'''
        with self._tray_status_lock:
            self._tray_status = tray_status

    def _set_tray_locked(self, tray_locked):
        '''Threadded Safe Set tray locked'''
        with self._tray_locked_lock:
            self._tray_locked = bool(tray_locked)

    def _set_disc_type(self, disc_type):
        '''Threadded Safe Set disc type'''
        with self._disc_type_lock:
            self._disc_type = disc_type

###########
##GETTERS##
###########
    def get_cfg_name(self):
        '''returns device config name READ ONLY SO THREAD SAFE'''
        return self._cfg_name

    def get_device(self):
        '''returns device READ ONLY SO THREAD SAFE'''
        return self._device

    def get_thread_run(self):
        '''return if thread is running'''
        return self._thread.is_alive()

    def get_drive_status(self):
        '''returns if the drive is open'''
        with self._drive_status_lock:
            drive_status = self._drive_status
        return drive_status

    def get_tray_status(self):
        '''returns if the tray is open'''
        with self._tray_status_lock:
            tray_status = self._tray_status
        return tray_status

    def get_tray_locked(self):
        '''returns if the tray is locked'''
        with self._tray_locked_lock:
            tray_locked = self._tray_locked
        return tray_locked

    def get_disc_type(self):
        '''returns the disc type if a disc is in the drive'''
        with self._disc_type_lock:
            disc_type = self._disc_type
        return disc_type

##########
##CHECKS##
##########
    @abstractmethod
    def check_tray(self):
        '''check the status of the disc tray'''
        pass

    @abstractmethod
    def _check_disc_type(self, sleep_time=1.0):
        '''Will return the size of the disc'''
        pass

    # @abstractmethod
    # def _check_audio_disc_information(self):
    #     '''Will return if drive is open or it will return a string of the error'''
    #     pass

################
##TRAYCONTROLS##
################

    @abstractmethod
    def open_tray(self):
        '''Send Command to open the tray'''
        pass

    @abstractmethod
    def close_tray(self):
        '''Send Command to close the tray'''
        pass

    @abstractmethod
    def lock_tray(self):
        '''Send Command to lock the tray'''
        pass

    @abstractmethod
    def unlock_tray(self):
        '''Send Command to unlock the tray'''
        pass

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
                        self._audio_rip()
                    elif self.get_disc_type() == "bluray" or self.get_disc_type() == "dvd":
                        self._set_drive_status("ripping video disc")
                        self._video_rip()
                    self.open_tray()
                    self.check_tray()
            self.unlock_tray()
            if not self._thread_run:
                return

    @abstractmethod
    def _audio_rip(self):
        '''script to rip an audio cd'''
        pass

    @abstractmethod
    def _video_rip(self):
        '''script to rip video disc'''
        pass
