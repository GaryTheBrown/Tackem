'''shared info between ripper systems'''

import time
from subprocess import DEVNULL, PIPE, Popen


class FileSubsystem:
    '''Disc and ISO SUbsystem'''

    def _get_udfInfo(self, in_file: str) -> dict:
        '''Grabs the relevent Data from UDF images'''
        list = {}
        process = Popen(["udfinfo", in_file], stdout=PIPE, stderr=DEVNULL)
        part_list = []
        while len(part_list) == 0:
            part_list = process.communicate()[0].decode('utf-8').split("\n")
            time.sleep(1)

        print(part_list)
        for item in part_list:
            print(item)
            list[item.split("=")[0]] = item.split("=")[1]
            if "udfrev" in list:
                break
        if process.returncode != 0:
            return {"disc_type":"audiocd"}

        return {
            'label':list['label'],
            'uuid':list['uuid'],
            'type':"bluray" if list['udfrev'] == "2.50" else "dvd"
        }

    def pass_to_next_system(self):
        '''Passes the disc's files through to the next system (converter/library)'''

class RipperSubSystem():
    '''Ripper Subsystem controller'''

    def __init__(self, in_file: str):
        self._in_file = in_file

        self._ripping_track = None
        self._ripping_file = 0
        self._ripping_total = 0
        self._ripping_max = 0
        self._ripping_file_p = 0.0
        self._ripping_total_p = 0.0

###########
##GETTERS##
###########
    def get_ripping_data(self) -> dict:
        '''returns the data as dict for html'''
        return {
            'track': self._ripping_track,
            'file': self._ripping_file,
            'total': self._ripping_total,
            'max': self._ripping_max,
            'file_percent': self._ripping_file_p,
            'total_percent': self._ripping_total_p
        }
