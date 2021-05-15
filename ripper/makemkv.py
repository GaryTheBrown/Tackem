"""MakeMKV ripping controller"""
import json
import os
from pathlib import Path
from typing import List
from typing import Optional

import pexpect

from config import CONFIG
from data.disc_type import make_disc_type
from data.disc_type.base import DiscType
from data.video_track_type.base import VideoTrackType
from database.ripper.video_convert import RipperVideoConvertInfo
from database.ripper.video_info import RipperVideoInfo
from libs.file import File
from ripper.disc_api import DiscAPI
from ripper.events import RipperEvent
from ripper.subsystems import RipperSubSystem

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
        info = RipperVideoInfo.do_select().where(RipperVideoInfo.id == db_id)
        if info is None:
            return ids

        if info.iso_file:
            self._in_file = File.location(
                info.iso_file,
                CONFIG["ripper"]["locations"]["iso"].value,
            )

        disc_rip_info: Optional[DiscType] = None
        if info.rip_data is None:
            disc_rip_info = DiscAPI.find_disctype(info.uuid, info.label)

            if disc_rip_info is None:
                info.data_disc = self.makemkv_info_from_disc()
                info.save()
        else:
            disc_rip_info = make_disc_type(json.loads(info.rip_data))

        temp_dir = File.location(f"{CONFIG['ripper']['locations']['ripping'].value}{str(db_id)}/")

        if isinstance(disc_rip_info, DiscType):
            self._track_data = True
            for idx, track in enumerate(disc_rip_info.tracks):
                if isinstance(track, VideoTrackType):
                    if track.track_type in CONFIG["ripper"]["videoripping"]["torip"].value:
                        self._makemkv_backup_from_disc(temp_dir, idx)
                        ids.append(
                            self.__pass_single_to_converter(
                                info.id,
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
                        info.id,
                        idx,
                        ("/" + "/".join(path.parts[1:])),
                        f"{info.label}: Track {idx}",
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

        data = {"track_count": tcount, "disc_info": cinfo, "track_info": tinfo}
        json.loads(json.dumps(data).replace('\\"', ""))

    def __pass_single_to_converter(
        self, info_id: int, track_number: int, filename: str, label: str, track_data: str
    ) -> int:
        """creates the DB section and then passes it to the converter in the ripper"""
        info = RipperVideoConvertInfo.get_or_none(
            info_id == info_id, track_number == track_number, filename == filename
        )
        if info is None:
            info = RipperVideoConvertInfo()
            info.info_id = info_id
            info.track_number = track_number
            info.filename = filename
            info.label = label
            info.track_data = track_data
            info.save()

        RipperEvent.do("video_converter_add_single", info.id)

        return info.id
