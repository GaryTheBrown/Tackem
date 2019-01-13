'''Special Linux Drive Functions'''
import os
import shlex
from subprocess import DEVNULL, PIPE, Popen
from .video import Video

class VideoLinux(Video):
    '''Video Control ripper program self contained'''

##########
##CHECKS##
##########
    def _check_disc_information(self):
        '''Will return if disc is in drive (setting the UUID and label) or it will return False'''
        process = Popen(["blkid", self._device], stdout=PIPE, stderr=DEVNULL)
        returned_message = process.communicate()[0]
        process.wait()
        if not returned_message:
            return False
        message = shlex.split(returned_message.decode('utf-8').rstrip().split(": ")[1])
        uuid = message[0].split("=")[1]
        label = message[1].split("=")[1]
        self._set_disc_info(uuid, label)
        return True

################
##MAKEMKV CALL##
################
    def _makemkv_backup_from_disc(self, temp_dir, index=-1):
        '''Do the mkv Backup from disc'''
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
