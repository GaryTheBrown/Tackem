'''Special Linux Drive Functions'''
import fcntl
import os
import shlex
from subprocess import DEVNULL, PIPE, Popen
from .drive import Drive

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
            if return_value is 1: #no disk in tray
                return "empty"
            elif return_value is 2: #tray open
                return "open"
            elif return_value is 3: #reading tray
                return "reading"
            elif return_value is 4: #disk in tray
                return "loaded"
        return "unknown"

    def _check_disc_size(self):
        '''Will return the size of the disc or false if no disc in the drive'''
        if self.get_tray_status() != "loaded":
            return False
        with self._drive_lock:
            process = Popen(["blockdev", "--getsize64", self._device], stdout=PIPE, stderr=DEVNULL)
            returned_message = process.communicate()[0]
            process.wait()
            message = returned_message.decode('ascii').rstrip()
        self._set_disc_size(message)
        return True

    def _check_disc_information(self):
        '''Will return if disc is in drive (setting the UUID and label) or it will return False'''
        if self.get_tray_status() != "loaded":
            return False
        with self._drive_lock:
            process = Popen(["blkid", self._device], stdout=PIPE, stderr=DEVNULL)
            returned_message = process.communicate()[0]
            process.wait()
        if not returned_message:
            return False
        message = shlex.split(returned_message.decode('ascii').rstrip().split(": ")[1])
        uuid = message[0].split("=")[1]
        with self._disc_info_lock:
            self._disc_info['UUID'] = uuid
            self._disc_info['Label'] = message[1].split("=")[1]
        return True

    def _check_audio_disc_information(self):
        '''Will return if drive is open or it will return a string of the error'''
        if self.get_tray_status() != "loaded":
            return False
        with self._drive_lock:
            process = Popen(["cdrdao", "discid", "--device", self._device],
                            stdout=PIPE, stderr=DEVNULL)
            returned_message = process.communicate()[0].decode('ascii').rstrip().split("\n")
            process.wait()
        if not returned_message:
            return False
        disc_rip_info = {}
        for line in returned_message:
            disc_rip_info[line.split(":")[0]] = line.split(":")[1]

        self._set_disc_rip_info(disc_rip_info)
        return True

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

###############
#EXTERNAL APPS#
###############
    def _makemkv_info_from_disc(self):
        '''Get info from within makemkv from disc'''
        prog_args = [
            "makemkvcon",
            "-r",
            "--messages=-stdout",
            "--progress=-null",
            "info",
            "dev:" + self._device
        ]
        process = Popen(prog_args, stdout=PIPE, stderr=DEVNULL)
        returned_message = process.communicate()[0].decode('ascii').split("\n")
        process.wait()
        try:
            os.remove("wget-log")
            os.remove("wget-log.1")
        except OSError:
            pass

        return returned_message

    def _makemkv_backup_from_disc(self, temp_dir, index=-1):
        '''Do the mkv Backup from disc'''
        #TODO still needs to be converted to prefered codec
        try:
            os.mkdir(temp_dir)
        except OSError:
            pass

        if index == -1:
            index = "all"

        prog_args = [
            "makemkvcon",
            "-r",
            "--messages=-null",
            "--progress=-stdout",
            "mkv",
            "dev:" + self._device,
            str(index),
            temp_dir
        ]
        process = Popen(prog_args, stdout=DEVNULL, stderr=DEVNULL)
        process.communicate()
        process.wait()
        try:
            os.remove("wget-log")
            os.remove("wget-log.1")
        except OSError:
            pass

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
        temp_list = {}
        temp_list['label'] = "Drive " + str(i + 1)
        temp_list['link'] = hwinfo_item["device_files"].split(",")[0]
        temp_list['model'] = hwinfo_item["model"].replace('"', "")
        temp_list['features'] = hwinfo_item["features"].replace(" ", "").split(",")
        drives[hwinfo_item["unique_id"].replace(".", "")] = temp_list
    return drives
