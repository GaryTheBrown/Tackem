'''Special Linux Drive Functions'''
import fcntl
from libs.ripper.makemkv.linux import MakeMKVLinux
import os
from shlex import shlex
import time
from subprocess import DEVNULL, PIPE, Popen
from . import Drive

class DriveLinux(Drive):
    '''Drive Control ripper program self contained'''

##########
##CHECKS##
##########
    def check_tray(self):
        '''detect_tray reads status of the drive.'''
        with self._drive_lock:
            file_device = os.open(self._device, os.O_RDONLY | os.O_NONBLOCK)
            return_value = fcntl.ioctl(file_device, 0x5326)
            os.close(file_device)
            if return_value == 1:  # no disk in tray
                self.tray_status = "empty"
                self.disc_type = "none"
                self.drive_status = "idle"
            elif return_value == 2:  # tray open
                self.tray_status = "open"
                self.disc_type = "none"
                self.drive_status = "idle"
            elif return_value == 3:  # reading tray
                self.tray_status = "reading"
                self.disc_type = "none"
                self.drive_status = "loading disc"
            elif return_value == 4:  # disk in tray
                self.tray_status = "loaded"
            else:
                self.tray_status = "unknown"
                self.disc_type = "none"
                self.drive_status = "ERROR"

    def _check_disc_type(self, sleep_time: float = 1.0) -> bool:
        '''Will return the size of the disc'''
        with self._drive_lock:
            if not self._thread_run:
                return False
            if self.tray_status != "loaded":
                self.disc_type = "None"
                return False
            message = ""
            while message == "":
                process1 = Popen(["udevadm", "info", "--query=all", "--name=" + self._device],
                                 stdout=PIPE, stderr=DEVNULL)
                process2 = Popen(["grep", "ID_FS_TYPE="],
                                 stdin=process1.stdout, stdout=PIPE)
                message = process2.communicate()[0].decode('utf-8').replace("\n", "")
                if not self._thread_run:
                    self.unlock_tray()
                    return False
                time.sleep(float(sleep_time))
            file_format = message.rstrip().split("=")[1]
            if file_format == "udf":
                process3 = Popen(["udevadm", "info", "--query=all", "--name=" + self._device],
                                 stdout=PIPE, stderr=DEVNULL)
                process4 = Popen(["grep", "ID_FS_VERSION="], stdin=process3.stdout, stdout=PIPE)
                message = process4.communicate()[0]
                udf_version_str = message.decode(
                    'utf-8').rstrip().split("=")[1]
                udf_version_float = float(udf_version_str)
                if udf_version_float == 1.02:
                    self.disc_type = "dvd"
                elif udf_version_float >= 2.50:
                    self.disc_type = "bluray"
            else:
                self.disc_type = "audiocd"
            return True

    def _check_disc_information(self):
        '''Gets unique ID info for the disc'''
        process = Popen(["blkid", self._device], stdout=PIPE, stderr=DEVNULL)
        returned_message = process.communicate()[0]
        if not returned_message:
            return False
        message = shlex.split(returned_message.decode('utf-8').rstrip().split(": ")[1])
        self.disc_uuid = message[0].split("=")[1]
        self.disc_label = message[1].split("=")[1]
        if not self._thread_run:
            return False

        # run for a second through mplayer so it will stop any dd I/O errors
        if self._disc_type == "dvd":
            mplayer_process = Popen(["mplayer", "dvd://1", "-dvd-device", self._device, "-endpos",
                                     "1", "-vo", "null", "-ao", "null"], stdout=DEVNULL,
                                    stderr=DEVNULL)
            mplayer_process.wait()
        if not self._thread_run:
            return False

        # using DD to read the disc pass it to sha256 to make a unique code for searching by
        dd_process = Popen(["dd", "if=" + self._device, "bs=4M", "count=128", "status=none"],
                           stdout=PIPE, stderr=DEVNULL)
        sha256sum = Popen(["sha256sum"], stdin=dd_process.stdout, stdout=PIPE, stderr=DEVNULL)
        self.disc_sha256 = sha256sum.communicate()[0].decode('utf-8').replace("-", "").rstrip()

        return dd_process.returncode == 0 and self._thread_run

    # def _check_audio_disc_information(self):
    #     '''Gets unique info for audio disc'''
    #     if self.tray_status != "loaded":
    #         return False
    #     with self._drive_lock:
    #         process = Popen(["cdrdao", "discid", "--device", self._device],
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
    def open_tray(self):
        '''Send Command to open the tray'''
        with self._drive_lock:
            Popen(["eject", self._device],
                  stdout=DEVNULL, stderr=DEVNULL).wait()

    def close_tray(self):
        '''Send Command to close the tray'''
        with self._drive_lock:
            Popen(["eject", "-t", self._device],
                  stdout=DEVNULL, stderr=DEVNULL).wait()

    def lock_tray(self):
        '''Send Command to lock the tray'''
        with self._drive_lock:
            self._tray_locked = True
            Popen(["eject", "-i1", self._device],
                  stdout=DEVNULL, stderr=DEVNULL).wait()

    def unlock_tray(self):
        '''Send Command to unlock the tray'''
        with self._drive_lock:
            self._tray_locked = False
            Popen(["eject", "-i0", self._device],
                  stdout=DEVNULL, stderr=DEVNULL).wait()

##########
##Script##
##########
    def _audio_rip(self):
        '''script to rip an audio cd'''
        # self._ripper = AudioCDLinux(self.__db_id)

    def _video_rip(self):
        '''script to rip video disc'''
        self._ripper = MakeMKVLinux(self.__db_id)
