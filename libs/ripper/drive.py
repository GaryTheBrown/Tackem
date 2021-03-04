'''Drive controller'''
from libs.ripper.subsystems import FileSubsystem
from libs.ripper.makemkv import MakeMKV
from libs.database import Database
from data.database.ripper import VIDEO_INFO_DB
from libs.database.where import Where
from libs.database.messages import SQLUpdate, SQLSelect, SQLInsert
from libs.html_system import HTMLSystem
from data.config import CONFIG
from libs.config.list import ConfigList
import threading
import time
import json
import fcntl
import os
import time
from subprocess import DEVNULL, PIPE, Popen

class Drive(FileSubsystem):
    '''Master Section for the Drive controller'''

    def __init__(self, config: ConfigList):
        super().__init__()
        self.__config = config
        self.__device = config['link'].value

        self.__thread = threading.Thread(target=self.__run, args=())
        self.__thread.setName("Ripper Drive:" + self.__device)
        self.__thread_run = True

        self.__drive_status = "idle"
        self.__tray_status = "startup"
        self.__tray_locked = False

    @property
    def device(self) -> str:
        '''returns device READ ONLY SO THREAD SAFE'''
        return self.__device

    @property
    def name(self) -> str:
        '''returns the name'''
        name = self.__config['label'].value
        device = self.__config['link'].value
        return f"{name} ({device})" if name != "" and name != device else device

    @property
    def thread_run(self) -> bool:
        '''return if thread is running'''
        return self.__thread.is_alive()

    def start_thread(self):
        '''start the thread'''
        if not self.__thread.is_alive():
            self.__thread.start()
            return True
        return False

    def stop_thread(self):
        '''stop the thread'''
        if self.__thread.is_alive():
            self.__thread_run = False
            self.__thread.join()

##########
##Script##
##########
    def __run(self):
        ''' Loops through the standard ripper function'''
        while self.__thread_run:
            self.__check_tray()
            while not self.__wait_for_disc(timeout=15):
                if not self.__thread_run:
                    return
            self.__lock_tray()
            self.__drive_status = "checking disc type"
            if self.__check_disc():
                if not self.__thread_run:
                    self.__unlock_tray()
                    return
                if self._disc['type'] == "audiocd":
                    self.__drive_status = "ripping audio cd disc"
                    # self._ripper = AudioCD(self.__device)
                elif self._disc['type'] == "bluray" or self._disc['type'] == "dvd":
                    self._add_video_disc_to_database()
                    self.__drive_status = f"ripping {self._disc['type']} video disc"
                    self._ripper = MakeMKV(self.__device)
                self._ripper.call(self._db_id)
                self._ripper = None
                if not self.__thread_run:
                    self.__unlock_tray()
                    return
                self.__open_tray()
                self.__check_tray()
            self.__unlock_tray()
            if not self.__thread_run:
                return

    def __wait_for_disc(self, sleep_time=1.0, timeout=10):
        '''waits for the disc info to be found'''
        count = 0
        while self.__tray_status != "loaded":
            if count >= timeout:
                return False
            if not self.__thread_run:
                return False
            time.sleep(float(sleep_time))
            count += 1
            self.__check_tray()
        return True

    def __check_tray(self):
        '''detect_tray reads status of the drive.'''
        file__device = os.open(self.__device, os.O_RDONLY | os.O_NONBLOCK)
        return_value = fcntl.ioctl(file__device, 0x5326)
        os.close(file__device)
        if return_value == 1:  # no disk in tray
            self.__tray_status = "empty"
            self._disc['type'] = "none"
            self.__drive_status = "idle"
        elif return_value == 2:  # tray open
            self.__tray_status = "open"
            self._disc['type'] = "none"
            self.__drive_status = "idle"
        elif return_value == 3:  # reading tray
            self.__tray_status = "reading"
            self._disc['type'] = "none"
            self.__drive_status = "loading disc"
        elif return_value == 4:  # disk in tray
            self.__tray_status = "loaded"
        else:
            self.__tray_status = "unknown"
            self._disc['type'] = "none"
            self.__drive_status = "ERROR"

    def __check_disc(self):
        '''Will return the disc info'''
        if not self.__thread_run:
            return False
        if self.__tray_status != "loaded":
            self._disc['type'] = "None"
            return False

        #wait for disc ready
        process = Popen(
            ["udevadm", "info", "--query=all", f"--name={self.__device}"],
            stdout=PIPE,
            stderr=DEVNULL
        )
        message = process.communicate()[0].decode('utf-8')
        while message == "":
            if not self.__thread_run:
                self.__unlock_tray()
                return False
            time.sleep(float(1))
            message = process.communicate()[0].decode('utf-8')

        self._get_udfInfo(self.device)
        return True

    # def __check_audio_disc_information(self):
    #     '''Gets unique info for audio disc'''
    #     if self.tray_status != "loaded":
    #         return False
    #     with self.__drive_lock:
    #         process = Popen(["cdrdao", "discid", "--device", self.__device],
    #                         stdout=PIPE, stderr=DEVNULL)
    #         returned_message = process.communicate()[0].decode('utf-8').rstrip().split("\n")
    #         process.wait()
    #     if not returned_message:
    #         return False
    #     disc_rip_info = {}
    #     for line in returned_message:
    #         disc_rip_info[line.split(":")[0]] = line.split(":")[1]

    #     self.disc_rip_info = disc_rip_info
    #     return True


################
##TRAYCONTROLS##
################
    def __open_tray(self):
        '''Send Command to open the tray'''
        Popen(["eject", self.__device],
                stdout=DEVNULL, stderr=DEVNULL).wait()

    def __close_tray(self):
        '''Send Command to close the tray'''
        Popen(["eject", "-t", self.__device],
                stdout=DEVNULL, stderr=DEVNULL).wait()

    def __lock_tray(self):
        '''Send Command to lock the tray'''
        self.__tray_locked = True
        Popen(["eject", "-i1", self.__device],
                stdout=DEVNULL, stderr=DEVNULL).wait()

    def __unlock_tray(self):
        '''Send Command to unlock the tray'''
        self.__tray_locked = False
        Popen(["eject", "-i0", self.__device],
                stdout=DEVNULL, stderr=DEVNULL).wait()

##############
##HTML STUFF##
##############
    def api_data(self) -> dict:
        '''returns the data as json or dict for html'''
        return_dict = {
            "drivestatus": self.__drive_status,
            "traylock": self.__tray_locked,
            "ripping": False,
        }
        if self._ripper:
            return_dict.update(self._ripper.get_ripping_data())

        return return_dict
