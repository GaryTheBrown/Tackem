'''Special Linux Drive Functions'''
import json
import os
import pexpect
import shlex
from subprocess import DEVNULL, PIPE, Popen
from libs.file import File
from .video import Video


class VideoLinux(Video):
    '''Video Control ripper program self contained'''

#################
##MAKEMKV CALLS##
#################
    def _makemkv_backup_from_disc(self, temp_dir: str, index: int = -1, device: bool = True):
        '''Do the mkv Backup from disc'''
        try:
            File.mkdir(temp_dir)
        except OSError:
            pass

        if index == -1:
            index = "all"

        prog_args = [
            "makemkvcon",
            "-r",
            "--minlength=0",
            "--messages=-null",
            "--progress=-stdout",
            "--noscan",
            "mkv",
            f"dev:{self._device}" if device else f"iso:",
            str(index),
            temp_dir
        ]
        thread = pexpect.spawn(" ".join(prog_args), encoding='utf-8')

        cpl = thread.compile_pattern_list([
            pexpect.EOF,
            'PRGC:\d+,\d+,"Saving to MKV file"',
            'PRGV:\d+,\d+,\d+',
            'PRGC:\d+,\d+,"Analyzing seamless segments"'
        ])
        update_progress = False
        while True:
            i = thread.expect_list(cpl, timeout=None)
            if i == 0:  # EOF
                self._ripping_track = None
                break
            elif i == 1:
                self._ripping_track = int(
                    thread.match.group(0).split(":")[1].split(",")[1])
                update_progress = True
            elif i == 2:
                if update_progress:
                    values = thread.match.group(0).split(":")[1].split(",")
                    self._ripping_file = int(values[0])
                    self._ripping_total = int(values[1])
                    self._ripping_max = int(values[2])
                    self._ripping_file_p = round(
                        float(int(values[0]) / int(values[2]) * 100), 2)
                    self._ripping_total_p = round(
                        float(int(values[1]) / int(values[2]) * 100), 2)
            elif i == 3:
                update_progress = False
                self._ripping_file = self._ripping_max
                self._ripping_file_p = round(float(100), 2)
        try:
            os.remove("wget-log")
            os.remove("wget-log.1")
        except OSError:
            pass
