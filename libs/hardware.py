'''Class to get all Hardware info needed'''
import platform
from subprocess import DEVNULL, PIPE, Popen

class Hardware:
    '''Class to get all Hardware info needed'''

    DRIVES = {}
    @classmethod
    def disc_drives(cls) -> dict:
        '''issues the hwinfo command and passes the info back in a dict'''
        if cls.DRIVES:
            return cls.DRIVES
        if platform.system() == 'Linux':
            cls.DRIVES = cls.__disc_drive_linux()
            return

    @classmethod
    def __disc_drive_linux(cls) -> dict:
        '''issues the hwinfo command and passes the info back in a dict'''
        process = Popen(["hwinfo", "--cdrom"], stdout=PIPE, stderr=DEVNULL)
        returned_message = process.communicate()[0]
        devices = returned_message.decode('utf-8').rstrip().split("\n\n")
        device_list = []
        for device in devices:
            device_single_list = {}
            device_lines = device.split("\n")
            for device_line in device_lines[2:]:
                device_line_1 = device_line.lstrip().split(":", 1)
                title = device_line_1[0].lower().replace(" ", "_")
                info = device_line_1[1].strip()
                device_single_list[title] = info
            if device_single_list:
                device_list.append(device_single_list)

        drives = {}
        for hwinfo_item in device_list:
            temp = {}
            temp['label'] = hwinfo_item["device_files"].split(",")[0]
            temp['link'] = hwinfo_item["device_files"].split(",")[0]
            temp['model'] = hwinfo_item["model"].replace('"', "")
            temp['features'] = hwinfo_item["features"].replace(
                " ", "").split(",")
            udevadm_process = Popen(["udevadm", "info", "--query=all", "--name=" + temp['link']],
                                    stdout=PIPE, stderr=DEVNULL)
            grep_process = Popen(["grep", "ID_SERIAL="],
                                 stdin=udevadm_process.stdout, stdout=PIPE)
            message = grep_process.communicate()[0]
            uid = message.decode(
                'utf-8').rstrip().split("=")[1].replace("-0:0", "").replace("_", "-")
            drives[uid] = temp
        return drives
