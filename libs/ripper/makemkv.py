"""MakeMKV ripping controller"""
import json
import os
from pathlib import Path
from typing import List
from typing import Optional

import pexpect

from data.config import CONFIG
from data.database.ripper import VIDEO_CONVERT_DB
from data.database.ripper import VIDEO_INFO_DB as DB
from data.disc_type import make_disc_type
from data.disc_type.base import DiscType
from data.video_track_type.base import VideoTrackType
from libs.database import Database
from libs.database.messages.insert import SQLInsert
from libs.database.messages.select import SQLSelect
from libs.database.messages.update import SQLUpdate
from libs.database.where import Where
from libs.file import File
from libs.ripper.disc_api import DiscAPI
from libs.ripper.events import RipperEvent
from libs.ripper.subsystems import RipperSubSystem

ITEM_ATTRIBUTE_ID = [
    "Unknown",
    "Type",
    "Name",
    "LangCode",
    "LangName",
    "CodecId",
    "CodecShort",
    "CodecLong",
    "ChapterCount",
    "Duration",
    "DiskSize",
    "DiskSizeBytes",
    "StreamTypeExtension",
    "Bitrate",
    "AudioChannelsCount",
    "AngleInfo",
    "SourceFileName",
    "AudioSampleRate",
    "AudioSampleSize",
    "VideoSize",
    "VideoAspectRatio",
    "VideoFrameRate",
    "StreamFlags",
    "DateTime",
    "OriginalTitleId",
    "SegmentsCount",
    "SegmentsMap",
    "OutputFileName",
    "MetadataLanguageCode",
    "MetadataLanguageName",
    "TreeInfo",
    "PanelTitle",
    "VolumeName",
    "OrderWeight",
    "OutputFormat",
    "OutputFormatDescription",
    "SeamlessInfo",
    "PanelText",
    "MkvFlags",
    "MkvFlagsText",
    "AudioChannelLayoutName",
    "OutputCodecShort",
    "OutputConversionType",
    "OutputAudioSampleRate",
    "OutputAudioSampleSize",
    "OutputAudioChannelsCount",
    "OutputAudioChannelLayoutName",
    "OutputAudioChannelLayout",
    "OutputAudioMixDescription",
    "Comment",
    "OffsetSequenceId",
]


class MakeMKV(RipperSubSystem):
    """MakeMKV ripping controller"""

    def call(self, db_id: int) -> List[int]:
        """run the makemkv backup function MUST HAVE DATA IN THE DB"""
        ids = []
        msg = SQLSelect(DB, Where("id", db_id))
        Database.call(msg)

        if not isinstance(msg.return_data, dict):
            return ids

        if msg.return_data["iso_file"]:
            self._in_file = File.location(
                msg.return_data["iso_file"],
                CONFIG["ripper"]["locations"]["iso"].value,
            )

        disc_data = None
        disc_rip_info: Optional[DiscType] = None
        if msg.return_data["rip_data"] is None:
            disc_rip_info = DiscAPI.find_disctype(msg.return_data["uuid"], msg.return_data["label"])

            if disc_rip_info is None:
                disc_data = json.dumps(self.makemkv_info_from_disc())
                Database.call(
                    SQLUpdate(DB, Where("id", msg.return_data["id"]), disc_data=disc_data)
                )
        else:
            disc_rip_info = make_disc_type(json.loads(msg.return_data["rip_data"]))

        temp_dir = File.location(f"{CONFIG['ripper']['locations']['ripping'].value}{str(db_id)}/")

        if isinstance(disc_rip_info, DiscType):
            self._track_data = True
            for idx, track in enumerate(disc_rip_info.tracks):
                if isinstance(track, VideoTrackType):
                    if track.track_type in CONFIG["ripper"]["videoripping"]["torip"].value:
                        self._makemkv_backup_from_disc(temp_dir, idx)
                        ids.append(
                            self.__pass_single_to_converter(
                                msg.return_data["id"],
                                idx,
                                temp_dir + str(idx).zfill(2) + ".mkv",
                                disc_rip_info.track_title(idx),
                                track.json(),
                            )
                        )
        elif disc_rip_info is None:
            self._makemkv_backup_from_disc(temp_dir)
            for idx, path in enumerate(Path(temp_dir).rglob("*.mkv")):
                ids.append(
                    self.__pass_single_to_converter(
                        msg.return_data["id"],
                        idx,
                        ("/" + "/".join(path.parts[1:])),
                        f"{msg.return_data['label']}: Track {idx}",
                        "{}",
                    )
                )

        return ids

    def _makemkv_backup_from_disc(self, temp_dir: str, index: int = -1):
        """Do the mkv Backup from disc"""
        try:
            File.mkdir(temp_dir)
        except OSError:
            pass

        if index == -1:
            index = "all"

        infile = f"dev:{self._in_file}"
        if "/dev/sr" not in self._in_file:
            infile = f"iso:{File.location(self._in_file)}"
        prog_args = [
            "makemkvcon",
            "-r",
            "--minlength=0",
            "--messages=-null",
            "--progress=-stdout",
            "--noscan",
            "mkv",
            infile,
            str(index),
            temp_dir,
        ]

        thread = pexpect.spawn(" ".join(prog_args), encoding="utf-8")

        cpl = thread.compile_pattern_list(
            [
                pexpect.EOF,
                r'PRGC:\d+,\d+,"Saving to MKV file"',
                r"PRGV:\d+,\d+,\d+",
                r'PRGC:\d+,\d+,"Analyzing seamless segments"',
            ]
        )
        update_progress = False
        while True:
            i = thread.expect_list(cpl, timeout=None)
            if i == 0:  # EOF
                self._ripping_track = None
                break
            elif i == 1:
                self._ripping_track = int(thread.match.group(0).split(":", 1)[1].split(",")[1])
                update_progress = True
            elif i == 2:
                if update_progress:
                    values = thread.match.group(0).split(":", 1)[1].split(",")
                    self._ripping_file = int(values[0])
                    self._ripping_total = int(values[1])
                    self._ripping_max = int(values[2])
                    self._ripping_file_p = round(float(int(values[0]) / int(values[2]) * 100), 2)
                    self._ripping_total_p = round(float(int(values[1]) / int(values[2]) * 100), 2)
            elif i == 3:
                update_progress = False
                self._ripping_file = self._ripping_max
                self._ripping_file_p = round(float(100), 2)
        try:
            os.remove("wget-log")
            os.remove("wget-log.1")
        except OSError:
            pass

    def makemkv_info_from_disc(self) -> dict:
        """Do the mkv Backup from disc"""
        infile = f"dev:{self._in_file}"
        if "/dev/sr" not in self._in_file:
            infile = f"iso:{File.location(self._in_file)}"
        prog_args = [
            "makemkvcon",
            "-r",
            "info",
            infile,
        ]

        thread = pexpect.spawn(" ".join(prog_args), encoding="utf-8")

        cpl = thread.compile_pattern_list(
            [
                pexpect.EOF,
                r"TCOUNT:\d+",
                r'CINFO:\d+,\d+,"(.*?)"',
                r'TINFO:\d+,\d+,\d+,"(.*?)"',
                r'SINFO:\d+,\d+,\d+,\d+,"(.*?)"',
            ]
        )

        tcount = 0
        cinfo = {}
        tinfo = []
        while True:
            i = thread.expect_list(cpl, timeout=None)
            if i == 0:  # EOF
                break
            elif i == 1:  # TCOUNT
                tcount = int(thread.match.group(0).split(":")[1])
            elif i == 2:  # CINFO
                values = thread.match.group(0).split(":", 1)[1].split(",", 2)
                cinfo_id = int(values[0])
                value = values[2]
                cinfo[ITEM_ATTRIBUTE_ID[cinfo_id]] = str(value)
            elif i == 3:  # TINFO
                values = thread.match.group(0).split(":", 1)[1].split(",", 3)
                track_id = int(values[0])
                if len(tinfo) <= track_id:
                    tinfo.append({})
                info_id = int(values[1])
                value = values[3]
                tinfo[track_id][ITEM_ATTRIBUTE_ID[info_id]] = str(value)
            elif i == 4:  # SINFO
                values = thread.match.group(0).split(":", 1)[1].split(",", 4)
                track_id = int(values[0])
                if "streams" not in tinfo[track_id]:
                    tinfo[track_id]["streams"] = []
                stream_id = int(values[1])
                if len(tinfo[track_id]["streams"]) <= stream_id:
                    tinfo[track_id]["streams"].append({})
                info_id = int(values[2])
                value = values[4]
                tinfo[track_id]["streams"][stream_id][ITEM_ATTRIBUTE_ID[info_id]] = str(value)

        return {"track_count": tcount, "disc_info": cinfo, "track_info": tinfo}

    def __pass_single_to_converter(
        self, info_id: int, track_number: int, filename: str, label: str, track_data: str
    ) -> int:
        """creates the DB section and then passes it to the converter in the ripper"""
        if (
            Database.count(
                SQLSelect(
                    VIDEO_CONVERT_DB,
                    Where("info_id", info_id),
                    Where("track_number", track_number),
                    Where("filename", filename),
                )
            )
            == 0
        ):
            Database.call(
                SQLInsert(
                    VIDEO_CONVERT_DB,
                    info_id=info_id,
                    track_number=track_number,
                    filename=filename,
                    label=label,
                    track_data=track_data,
                )
            )

        msg = SQLSelect(
            VIDEO_CONVERT_DB,
            Where("info_id", info_id),
            Where("track_number", track_number),
            Where("filename", filename),
        )

        Database.call(msg)
        RipperEvent.do("video_converter_add_single", msg.return_data["id"])

        return msg.return_data["id"]
