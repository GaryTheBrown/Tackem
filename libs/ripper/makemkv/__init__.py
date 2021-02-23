'''MakeMKV ripping controller'''
from abc import ABCMeta, abstractmethod
from libs.ripper.disc_info_grabber import rip_data
from libs.database.messages import SQLUpdate
from libs.database.where import Where
from libs.database.messages import SQLSelect
from libs.file import File
import json
from libs.database import Database
from data.config import CONFIG
from libs.ripper.ripper_subsystem import RipperSubSystem
from libs.ripper.converter import create_video_converter_row
from data.database.ripper import VIDEO_INFO_DB as DB
from libs.ripper.data.disc_type import DiscType, make_disc_type
from libs.ripper.events import RipperEvents

class MakeMKV(RipperSubSystem, metaclass=ABCMeta):
    '''MakeMKV ripping controller'''

    def call_makemkv_backup(self, id: int) -> bool:
        '''run the makemkv backup function MUST HAVE DATA IN THE DB'''
        msg = SQLSelect(DB.name(), Where("id", id))
        Database.call(msg)

        if not isinstance(msg.return_data, dict):
            return False

        disc_rip_info = rip_data(msg.return_data)

        if msg.return_data['iso_file']:
            folder = CONFIG['ripper']['locations']['videoiso'].value
            self._device = f"{folder}{msg.return_data['iso_file']}"
        temp_location = File.location(CONFIG['ripper']['locations']['videoripping'].value)
        temp_dir = temp_location + str(self._disc_info_sha256)
        if isinstance(disc_rip_info, list):
            for idx, track in enumerate(disc_rip_info):
                if not isinstance(track, bool):
                    self._makemkv_backup_from_disc(temp_dir, idx, msg.return_data['iso_file'] == "")
        elif disc_rip_info is None:
            self._makemkv_backup_from_disc(temp_dir, device=msg.return_data['iso_file'] == "")

        Database.call(SQLUpdate(DB.name(), Where("id", id), ripped=True))

        if CONFIG['ripper']['converter']['enabled'].value:
            create_video_converter_row(
                id,
                disc_rip_info,
                CONFIG['ripper']['videoripping']['torip'].value
            )
            Database.call(SQLUpdate(DB.name(), Where("id", id), ready_to_convert=True))
            RipperEvents().converter.set()
        else:
            Database.call(SQLUpdate(DB.name(), Where("id", id), ready_to_rename=True))
            RipperEvents().renamer.set()

        return True

    @abstractmethod
    def _makemkv_backup_from_disc(self, temp_dir, index=-1, device: bool = True):
        '''Do the mkv Backup from disc'''
