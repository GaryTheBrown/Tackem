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
        #run for a second through mplayer so it will stop any dd I/O errors
        if self._disc_type == "dvd":
            mplayer_process = Popen(["mplayer", "dvd://1", "-dvd-device", self._device, "-endpos",
                                     "1", "-vo", "null", "-ao", "null"], stdout=DEVNULL, 
                                     stderr=DEVNULL)
            mplayer_process.wait()
        #using DD to read the disc pass it to sha256 to make a unique code for searching by
        dd_process = Popen(["dd", "if=" + self._device, "bs=4M", "count=128", "status=none"],
                           stdout=PIPE)
        sha256sum_process = Popen(["sha256sum"], stdin=dd_process.stdout, stdout=PIPE)
        sha256 = sha256sum_process.communicate()[0].decode('utf-8').replace("-", "").rstrip()
        dd_process.wait()
        sha256sum_process.wait()
        self._set_disc_info(uuid, label, sha256)
        return True

#################
##MAKEMKV CALLS##
#################
    def _makemkv_backup_from_disc(self, temp_dir, index=-1):
        '''Do the mkv Backup from disc'''
        try:
            os.mkdir(temp_dir)
        except OSError:
            pass
        with open(temp_dir + "/info.txt", "w") as text_file:
            string = "UUID: " + self.get_disc_info_uuid() + "\nLabel: " + self.get_disc_info_label()
            text_file.write(string)
        if index == -1:
            index = "all"

        prog_args = [
            "makemkvcon",
            "-r",
            "--minlength=0",
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
