'''MakeMKV ripping controller'''
import sys
from libs.ripper.disc_info_grabber import rip_data
from libs.database.where import Where
from libs.database.messages import SQLSelect
from libs.database import Database
from data.config import CONFIG
from libs.ripper.subsystems import RipperSubSystem
from data.database.ripper import VIDEO_INFO_DB as DB
import os
import pexpect
from libs.file import File
class MakeMKV(RipperSubSystem):
    '''MakeMKV ripping controller'''

    def call(self, db_id: int) -> bool:
        '''run the makemkv backup function MUST HAVE DATA IN THE DB'''
        msg = SQLSelect(DB, Where("db_", db_id))
        Database.call(msg)

        if not isinstance(msg.return_data, dict):
            return False

        disc_rip_info = rip_data(msg.return_data)

        if msg.return_data['iso_file']:
            self._in_file = File.location(
                msg.return_data['iso_file'],
                CONFIG['ripper']['locations']['videoiso'].value
            )

        temp_dir = File.location(f"{CONFIG['ripper']['locations']['videoripping'].value}{str(id)}/")
        device = msg.return_data['iso_file'] == ""
        if isinstance(disc_rip_info, list):
            self._track_data = True
            for idx, track in enumerate(disc_rip_info):
                if not isinstance(track, bool):
                    self._makemkv_backup_from_disc(temp_dir, idx, device)
        elif disc_rip_info is None:
            self._makemkv_backup_from_disc(temp_dir, device=device)

        comp_dir = File.location(f"{CONFIG['ripper']['locations']['videoripped'].value}{str(id)}/")
        File.move(temp_dir, comp_dir)

        #TODO calls the next system

        if not device and CONFIG['ripper']['iso']['removeiso'].value:
            File.rm(File.location(self._in_file))

        return True

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
            f"dev:{self._in_file}" if device else f"iso:{File.location(self._in_file)}",
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
                self._ripping_track = int(thread.match.group(0).split(":")[1].split(",")[1])
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
