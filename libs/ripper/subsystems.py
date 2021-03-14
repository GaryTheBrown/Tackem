"""shared info between ripper systems"""
from libs.database.messages.insert import SQLInsert
from libs.database.messages.update import SQLUpdate
from libs.database import Database
from libs.database.where import Where
from data.database.ripper import VIDEO_INFO_DB
from libs.database.messages.select import SQLSelect
from libs.file import File
from subprocess import DEVNULL, PIPE, Popen


class FileSubsystem:
    """Disc and ISO SUbsystem"""

    def __init__(self):
        self._disc = {"type": "none", "uuid": "", "label": ""}

        self._db_id = None
        self._ripper = None  # whatever the ripper is makemkv and cd ripper

    def _add_video_disc_to_database(self, filename: str = ""):
        """sets up the DB stuff for disc"""
        msg = SQLSelect(
            VIDEO_INFO_DB,
            Where("uuid", self._disc["uuid"]),
            Where("label", self._disc["label"]),
            Where("disc_type", self._disc["type"]),
        )
        Database.call(msg)
        if isinstance(msg.return_data, dict):
            if isinstance(filename, str) and filename != "":
                Database.call(
                    SQLUpdate(
                        VIDEO_INFO_DB,
                        Where("id", msg.return_data["id"]),
                        iso_file=filename,
                    )
                )
            self._db_id = msg.return_data["id"]
            return

        Database.call(
            SQLInsert(
                VIDEO_INFO_DB,
                iso_file=filename,
                uuid=self._disc["uuid"],
                label=self._disc["label"],
                disc_type=self._disc["type"],
            )
        )

        msg = SQLSelect(
            VIDEO_INFO_DB,
            Where("uuid", self._disc["uuid"]),
            Where("label", self._disc["label"]),
            Where("disc_type", self._disc["type"]),
        )
        Database.call(msg)
        self._db_id = msg.return_data["id"]

    def _get_udfInfo(self, in_file: str):
        """Grabs the relevent Data from UDF images"""
        list = {}
        process = Popen(
            ["udfinfo", File.location(in_file)], stdout=PIPE, stderr=DEVNULL
        )
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

    ###########
    ##GETTERS##
    ###########
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
