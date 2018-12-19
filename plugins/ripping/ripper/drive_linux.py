'''Special Linux Drive Functions'''
import fcntl
import os
from subprocess import DEVNULL, PIPE, Popen
from .drive import Drive

class DriveLinux(Drive):
    '''Drive Control ripper program self contained'''

    def check_tray(self):
        '''detect_tray reads status of the drive.'''
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
        with self._drive_lock:
            process = Popen(["blockdev", "--getsize64", self._device], stdout=PIPE, stderr=DEVNULL)
            returned_message = process.communicate()[0]
            process.wait()
            message = returned_message.decode('ascii').rstrip()
        self._set_disc_size(message)
        return True

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
