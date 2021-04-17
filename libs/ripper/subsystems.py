"""shared info between ripper systems"""
from shutil import which
from subprocess import PIPE
from subprocess import Popen

from database.ripper_video_info import VideoInfo
from libs.file import File


class FileSubsystem:
    """Disc and ISO SUbsystem"""

    def __init__(self):
        self._disc = {"type": "none", "uuid": "", "label": ""}

        self._db_id = None
        self._ripper = None  # whatever the ripper is makemkv and cd ripper

    def _add_video_disc_to_database(self, filename: str = ""):
        """sets up the DB stuff for disc"""
        info = (
            VideoInfo.do_select()
            .where(
                VideoInfo.uuid == self._disc["uuid"],
                VideoInfo.label == self._disc["label"],
                VideoInfo.disc_type == self._disc["type"],
            )
            .get()
        )
        if isinstance(VideoInfo, info):
            if isinstance(filename, str) and filename != "":
                info.filename = filename
                info.save()
            self._db_id = info.id
            return

        info = VideoInfo()
        info.uuid == self._disc["uuid"],
        info.label == self._disc["label"],
        info.disc_type == self._disc["type"],
        info.filename == filename
        info.save()
        self._db_id = info.id
        return

    def _get_udfInfo(self, in_file: str):
        """Grabs the relevent Data from UDF images"""
        list = {}
        process = Popen([which("udfinfo"), File.location(in_file)], stdout=PIPE)
        part_list = process.communicate()[0].decode("utf-8").split("\n")[:-1]

        for item in part_list:
            list[item.split("=")[0]] = item.split("=")[1]
        if process.returncode != 0:
            self._disc = {"disc_type": "audiocd"}

        self._disc = {
            "label": list["label"],
            "uuid": list["uuid"],
            "type": "bluray" if list["udfrev"] == "2.50" else "dvd",
        }


class RipperSubSystem:
    """Ripper Subsystem controller"""

    def __init__(self, in_file: str = ""):
        self._in_file = in_file
        self._track_data = False
        self._ripping_track = False
        self._ripping_file = 0
        self._ripping_total = 0
        self._ripping_max = 0
        self._ripping_file_p = 0.0
        self._ripping_total_p = 0.0

    def get_ripping_data(self) -> dict:
        """returns the data as dict for html"""
        ripping_track = "N/A" if self._ripping_track is False else self._ripping_track
        return {
            "trackdata": self._track_data,
            "ripping": self._ripping_track,
            "max": self._ripping_max,
            "trackpercent": self._ripping_file_p,
            "trackvalue": self._ripping_file,
            "tracklabel": f"Track {ripping_track} ({self._ripping_file_p}%)",
            "totalpercent": self._ripping_total_p,
            "totalvalue": self._ripping_total,
            "totallabel": f"Total ({self._ripping_total_p}%)",
        }
