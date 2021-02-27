'''Special Linux Drive Functions'''
from libs.database.where import Where
from data.database.ripper import VIDEO_INFO_DB
from libs.database.messages.update import SQLUpdate
from libs.database import Database
from libs.ripper.disc_info_grabber import gen_sha256_linux
from data.config import CONFIG
from libs.file import File
from libs.ripper.ISO.iso import ISORipper
from subprocess import DEVNULL, PIPE, Popen

from libs.ripper.makemkv.linux import MakeMKVLinux

class ISORipperLinux(ISORipper):
    '''Drive Control ripper program self contained'''

##########
##Script##
##########
    def _audio_rip_setup(self):
        '''script to rip an audio cd'''
        # self._ripper = AudioCDLinux(self.get_device(), self._thread.getName(),
                                    # self._set_drive_status, self._thread_run)

    def _video_rip_setup(self):
        '''script to rip video disc'''

        file = File.location(
            self._db_data['iso_file'],
            CONFIG['ripper']['locations']['videoiso'].value
        )

        data = self._get_udfInfo(file)
        sha256=gen_sha256_linux(file)

        Database.call(
            SQLUpdate(
                VIDEO_INFO_DB.name(),
                Where("id", self._db_data['id']),
                sha256=sha256,
                label=data['label'],
                uuid=data['uuid'],
                disc_type="bluray" if data['udfrev'] == "2.50" else "dvd"
            )
        )
        self._ripper = MakeMKVLinux("")

    def _get_udfInfo(self, in_file: str) -> dict:
        '''Grabs the relevent Data from UDF images'''
        process = Popen(["udfinfo", in_file], stdout=PIPE, stderr=DEVNULL)
        if process.returncode != 0:
            return {}

        list = process.communicate()[0].decode('utf-8').split("\n")
        output = {}
        for item in list:
                if item == "":
                        continue
                new = item.split("=")
                if new[0] in ["label", "uuid", "udfrev"]:
                    output[new[0]] = new[1]

        return output
