'''MakeMKV ripping controller'''
from abc import ABCMeta, abstractmethod
from libs.database.messages.insert import SQLInsert
from libs.database.messages.update import SQLUpdate
from libs.database.where import Where
from libs.database.messages.select import SQLSelect
from typing import Callable
from libs.file import File
import json
from libs.database import Database
from data.config import CONFIG
from libs.ripper.ripper_subsystem import RipperSubSystem
from libs.ripper.converter import create_video_converter_row
from libs.ripper.disc_api import apiaccess_video_disc_id
from data.database.ripper import VIDEO_INFO_DB_INFO as INFO_DB
from libs.ripper.data.disc_type import make_disc_type
from libs.ripper.events import RipperEvents


class MakeMKV(RipperSubSystem, metaclass=ABCMeta):
    '''MakeMKV ripping controller'''

    def __init__(
        self,
        device: str,
        thread_name: str,
        set_drive_status: Callable,
        thread_run: bool,
    ):
        super().__init__(device, thread_name, set_drive_status, thread_run)
        self._disc_rip_info = None
        self._db_data = None
        self._db_id = None

#######################
##DATABASE & API CALL##
#######################
    def _check_db_and_api_for_disc_info(
        self,
        uuid: str,
        label: str,
        sha256: str,
        disc_type: str,
    ):
        '''checks the DB and API for the Disc info'''


        msg = SQLSelect(
            INFO_DB.name(),
            Where("uuid", uuid),
            Where("label", label),
            Where("sha256", sha256),
            Where("disc_type", disc_type),
        )
        Database.call(msg)

        if isinstance(msg.return_data, dict):
            Database.call(
                SQLUpdate(
                    INFO_DB.name(),
                    Where(
                        "id",
                        msg.return_data['id']
                    ),
                    ripped=False,
                    ready_to_convert=False,
                    ready_to_rename=False,
                    ready_for_library=False,
                    completed=False
                )
            )
        else:
            Database.call(
                SQLInsert(
                    INFO_DB.name(),
                    uuid=self.__uuid,
                    label=self.__label,
                    sha256=self.__sha256,
                    disc_type=self.__disc_type,
                    ripped=False,
                    ready_to_convert=False,
                    ready_to_rename=False,
                    ready_for_library=False,
                    completed=False
                )
            )

        Database.call(msg)
        self._db_data = msg.return_data
        self._db_id = msg.return_data['id']
        rip_data_json = msg.return_data['rip_data']
        if rip_data_json is not None:
            self._disc_rip_info = make_disc_type(json.loads(rip_data_json))
            return

        rip_list = apiaccess_video_disc_id(self.__uuid, self.__label)
        if isinstance(rip_list, str):
            self._disc_rip_info = make_disc_type(json.loads(rip_list))
            Database.call(
                SQLUpdate(
                    INFO_DB.name(),
                    Where("id", self._db_id),
                    rip_data=rip_list
                )
            )

#################
##MAKEMKV CALLS##
#################

    def _call_makemkv_backup(self):
        '''run the makemkv backup function thread safe'''
        temp_location = File.location(CONFIG['ripper']['locations']['videoripping'].value)
        temp_dir = temp_location + str(self._disc_info_sha256)
        if isinstance(self._disc_rip_info, list):
            for idx, track in enumerate(self._disc_rip_info):
                if not isinstance(track, bool):
                    self._makemkv_backup_from_disc(temp_dir, idx)
                    if not self._thread_run:
                        return False
        elif self._disc_rip_info is None:
            self._makemkv_backup_from_disc(temp_dir)
        self._set_drive_status("idle")
        Database.call(
            SQLUpdate(
                INFO_DB.name(),
                Where("id", self._db_id),
                ripped=True
            )
        )
        return True

    @abstractmethod
    def _makemkv_backup_from_disc(self, temp_dir, index=-1, device: bool = True):
        '''Do the mkv Backup from disc'''

#######################
##SEND TO NEXT SYSTEM##
#######################
    def _send_to_next_system(self):
        '''method to send info to the next step in the process'''
        config = CONFIG['ripper']
        if config['converter']['enabled'].value:
            create_video_converter_row(
                self._db_id,
                self._disc_rip_info,
                config['videoripping']['torip'].value
            )
            Database.call(
                SQLUpdate(
                    INFO_DB.name(),
                    Where("id", self._db_id),
                    ready_to_convert=True
                )
            )
            RipperEvents().converter.set()
        else:
            Database.call(
                SQLUpdate(
                    INFO_DB.name(),
                    Where("id", self._db_id),
                    ready_to_rename=True
                )
            )
            RipperEvents().renamer.set()
##########
##Script##
##########

    def run(self):
        '''script to rip video disc'''
        self._set_drive_status("Get disc unique data")
        if not self._check_disc_information():
            return
        if not self._thread_run:
            return
        self._set_drive_status("checking info")
        self._check_db_and_api_for_disc_info()
        if not self._thread_run:
            return
        self._set_drive_status("Ripping Disc")
        if not self._call_makemkv_backup():
            return
        if self._disc_rip_info:
            self._send_to_next_system()
