'''MakeMKV ripping controller'''
from abc import ABCMeta, abstractmethod
from libs.database.messages.update import SQLUpdate
from libs.database.where import Where
from libs.database.messages.select import SQLSelect
from libs.file import File
import json
from libs.database import Database
from data.config import CONFIG
from libs.ripper.ripper_subsystem import RipperSubSystem
from libs.ripper.converter import create_video_converter_row
from data.database.ripper import VIDEO_INFO_DB_INFO as INFO_DB
from libs.ripper.data.disc_type import make_disc_type
from libs.ripper.events import RipperEvents

class MakeMKV(RipperSubSystem, metaclass=ABCMeta):
    '''MakeMKV ripping controller'''

    def __init__(self, device: str, thread_name: str, thread_run: bool):
        super().__init__(device, thread_name, thread_run)

    #################
    ##MAKEMKV CALLS##
    #################
    def call_makemkv_backup(self, id: int) -> bool:
        '''run the makemkv backup function MUST HAVE DATA IN THE DB'''
        msg = SQLSelect(INFO_DB.name(), Where("id", id))
        Database.call(msg)

        if not self._thread_run:
            return False

        if not isinstance(msg.return_data, dict):
            return False

        Database.call(
            SQLUpdate(
                INFO_DB.name(),
                Where("id", id),
                ripped=False,
                ready_to_convert=False,
                ready_to_rename=False,
                ready_for_library=False,
                completed=False
            )
        )

        if not self._thread_run:
            return False

        Database.call(msg)
        rip_data_json = msg.return_data['rip_data']
        if rip_data_json is not None:
            disc_rip_info = make_disc_type(json.loads(rip_data_json))

        if not self._thread_run:
            return False

        if msg.return_data['filename']:
            folder = CONFIG['ripper']['locations']['videoiso'].value
            self._device = f"{folder}{msg.return_data['filename']}"
        temp_location = File.location(CONFIG['ripper']['locations']['videoripping'].value)
        temp_dir = temp_location + str(self._disc_info_sha256)
        if isinstance(disc_rip_info, list):
            for idx, track in enumerate(disc_rip_info):
                if not isinstance(track, bool):
                    self._makemkv_backup_from_disc(temp_dir, idx)
                    if not self._thread_run:
                        return False
        elif disc_rip_info is None:
            self._makemkv_backup_from_disc(temp_dir)

        Database.call(
            SQLUpdate(
                INFO_DB.name(),
                Where("id", id),
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
    #TODO move this out to somewhere for use by ISO and Drive Ripper
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
