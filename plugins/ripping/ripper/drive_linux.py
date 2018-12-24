'''Special Linux Drive Functions'''
import fcntl
import os
import time
from subprocess import DEVNULL, PIPE, Popen
from .drive import Drive
from .video_linux import VideoLinux

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
            if return_value == 1: #no disk in tray
                self._set_tray_status("empty")
            elif return_value == 2: #tray open
                self._set_tray_status("open")
            elif return_value == 3: #reading tray
                self._set_tray_status("reading")
            elif return_value == 4: #disk in tray
                self._set_tray_status("loaded")
            else:
                self._set_tray_status("unknown")

    def _check_disc_type(self, sleep_time=1.0):
        '''Will return the size of the disc'''
        message = ""
        with self._drive_lock:
            while message == "":
                if not self._thread_run:
                    return False
                if self.get_tray_status() != "loaded":
                    return False
                process = Popen(["lsblk", "-no", "FSTYPE", self._device],
                                stdout=PIPE, stderr=DEVNULL)
                returned_message = process.communicate()[0]
                process.wait()
                message = returned_message.decode('ascii').rstrip()
                time.sleep(float(sleep_time))
        self._set_disc_type(message)
        return True

    # def _check_audio_disc_information(self):
    #     '''Will return if drive is open or it will return a string of the error'''
    #     if self.get_tray_status() != "loaded":
    #         return False
    #     with self._drive_lock:
    #         process = Popen(["cdrdao", "discid", "--device", self._device],
    #                         stdout=PIPE, stderr=DEVNULL)
    #         returned_message = process.communicate()[0].decode('ascii').rstrip().split("\n")
    #         process.wait()
    #     if not returned_message:
    #         return False
    #     disc_rip_info = {}
    #     for line in returned_message:
    #         disc_rip_info[line.split(":")[0]] = line.split(":")[1]

    #     self._set_disc_rip_info(disc_rip_info)
    #     return True

################
##TRAYCONTROLS##
################
    def open_tray(self):
        '''Send Command to open the tray'''
        with self._drive_lock:
            Popen(["eject", self._device]).wait()

    def close_tray(self):
        '''Send Command to close the tray'''
        with self._drive_lock:
            Popen(["eject", "-t", self._device]).wait()

    def lock_tray(self):
        '''Send Command to lock the tray'''
        with self._drive_lock:
            Popen(["eject", "-i1", self._device]).wait()

    def unlock_tray(self):
        '''Send Command to unlock the tray'''
        with self._drive_lock:
            Popen(["eject", "-i0", self._device]).wait()


##########
##Script##
##########
    def _audio_rip(self):
        '''script to rip an audio cd'''
        pass
        # self._check_audio_disc_information()

    def _video_rip(self):
        '''script to rip video disc'''
        video_ripper = VideoLinux(self.get_device(), self._config, self._db, self._thread.getName())
        video_ripper.run()

###############
#EXTERNAL APPS#
###############
def get_hwinfo_linux():
    '''issues the hwinfo command and passes the info back in a dict'''
    process = Popen(["hwinfo", "--cdrom"], stdout=PIPE, stderr=DEVNULL)
    returned_message = process.communicate()[0]
    process.wait()
    devices = returned_message.decode('ascii').rstrip().split("\n\n")
    device_list = []
    for device in devices:
        device_single_list = {}
        device_lines = device.split("\n")
        for device_line in device_lines[2:]:
            device_line_1 = device_line.lstrip().split(":", 1)
            title = device_line_1[0].lower().replace(" ", "_")
            info = device_line_1[1].strip()
            device_single_list[title] = info
        device_list.append(device_single_list)
    drives = {}
    for i, hwinfo_item in enumerate(device_list):
        drive_address = hwinfo_item["device_files"].split(",")[0]
        temp_list = {}
        temp_list['label'] = "Drive " + str(i + 1) + " (" + drive_address + ")"
        temp_list['link'] = hwinfo_item["device_files"].split(",")[0]
        temp_list['model'] = hwinfo_item["model"].replace('"', "")
        temp_list['features'] = hwinfo_item["features"].replace(" ", "").split(",")
        drives[hwinfo_item["unique_id"].split(".")[1]] = temp_list
    return drives
