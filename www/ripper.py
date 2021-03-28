"""Ripper Root pages"""
import json

import cherrypy

from data.config import CONFIG
from data.database.ripper import VIDEO_INFO_DB
from libs.authenticator import Authentication
from libs.database import Database
from libs.database.messages.select import SQLSelect
from libs.database.where import Where
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE
from libs.ripper import Ripper
from www.partial.uploads import PartialsUpload


class RipperRoot(HTMLTEMPLATE):
    """ROOT OF PLUGINS WEBUI HERE"""

    @cherrypy.expose
    def index(self) -> str:
        """index of Ripper"""
        Authentication.check_auth()
        return self._template(
            HTMLSystem.part(
                "pages/ripper/index",
                DRIVES=self.__drives_data(),
                UPLOADPARTIAL=PartialsUpload.iso(),
                ISOCOUNT=len(Ripper.isos),
                ISOTHREADLIMIT=CONFIG["ripper"]["iso"]["threadcount"].value,
                ISOTEMPLATE=HTMLSystem.open("partial/ripper/iso"),
                VIDEOCONVERTERCOUNT=len(Ripper.video_converters),
                VIDEOCONVERTERTHREADLIMIT=CONFIG["ripper"]["converter"]["threadcount"].value,
                VIDEOCONVERTERTEMPLATE=HTMLSystem.open("partial/ripper/videoconverter"),
            ),
            javascript="js/ripper.js",
        )

    def __drives_data(self) -> str:
        """returns the group of drives html"""
        html = ""
        for drive_index, drive_obj in enumerate(Ripper.drives):
            html += HTMLSystem.part(
                "partial/ripper/drive",
                DRIVENUMBER=str(drive_index),
                NAME=drive_obj.name,
            )
        return html

    @cherrypy.expose
    def disc(self, db_id: int) -> str:
        """Shows the Disc Info with ability to edit locally made if not on API or uploaded"""
        # Authentication.check_auth()
        msg = SQLSelect(VIDEO_INFO_DB, Where("id", db_id))
        Database.call(msg)
        if isinstance(msg.return_data, list):
            raise cherrypy.HTTPError(status=404)

        return self._template(self.__disc_info(db_id, msg.return_data))

    def __disc_info(self, db_id: int, data: dict) -> str:
        """Generates the page for when no data exists"""
        # if data["rip_data_download"]:
        # pass # need to deal with right panel here

        clean = data["disc_data"].replace('\\"', "")
        disc_data = json.loads(clean)
        # rip_data = data["rip_data"]

        track_html = ""
        for index, track in enumerate(disc_data["track_info"]):
            track_html += self.__track_info(index, track)

        return HTMLSystem.part(
            "pages/ripper/disc",
            DBID=db_id,
            DISCNAME=disc_data["disc_info"]["Name"],
            DISCLANGUAGE=disc_data["disc_info"]["MetadataLanguageName"],
            ISOFILE=data["iso_file"],
            UUID=data["uuid"].upper(),
            LABEL=data["label"],
            DISCTYPE=data["disc_type"].upper(),
            TRACKHTML=track_html,
            # DISCDATAJSON=data["disc_data"],
            # RIPDATAJSON=data["rip_data"],
        )

    def __track_info(self, index: int, data: dict) -> str:
        """Generates track info section"""

        stream_html = ""
        for stream in data["streams"]:
            stream_html += self.__stream_info(stream)

        return HTMLSystem.part(
            "partial/ripper/trackinfo",
            INDEX=str(index).zfill(2),
            DURATION=data["Duration"],
            CHAPTERS=data["ChapterCount"],
            STREAMS=stream_html,
        )

    def __stream_info(self, data: dict) -> str:
        """Generates the stream info section"""
        if data["Type"] == "Video":
            return HTMLSystem.part(
                "partial/ripper/videostream",
                TYPE=data["Type"],
                VIDEOSIZE=data["VideoSize"],
                VIDEOASPECTRATIO=data["VideoAspectRatio"],
                VIDEOFRAMERATE=data["VideoFrameRate"],
            )
        if data["Type"] == "Audio":
            return HTMLSystem.part(
                "partial/ripper/audiostream", TYPE=data["Type"], TREEINFO=data["TreeInfo"]
            )
        if data["Type"] == "Subtitles":
            return HTMLSystem.part(
                "partial/ripper/subtitlestream",
                TYPE=data["Type"],
                LANGNAME=data["LangName"],
                CODECLONG=data["CodecLong"],
            )
