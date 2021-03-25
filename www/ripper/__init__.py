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
    def index(self):
        """index of Ripper"""
        Authentication.check_auth()
        return self._template(
            HTMLSystem.part(
                "pages/ripper/index",
                DRIVES=self.drives_data(),
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

    @cherrypy.expose
    def disc(self, db_id: int):
        """Shows the Disc Info with ability to edit locally made if not on API or uploaded"""
        # Authentication.check_auth()
        msg = SQLSelect(VIDEO_INFO_DB, Where("id", db_id))
        Database.call(msg)
        if isinstance(msg.return_data, list):
            raise cherrypy.HTTPError(status=404)

        if msg.return_data["rip_data_download"]:
            return self._template(self.__disc_locked_info(db_id, msg.return_data))
        else:
            return self._template(self.__disc_no_info(db_id, msg.return_data))

    def __disc_locked_info(self, db_id: int, data: dict):
        """Generates the page for when data exists from API"""
        return "LOCKED"

    def __disc_no_info(self, db_id: int, data: dict):
        """Generates the page for when no data exists"""

        clean = data["disc_data"].replace('\\"', "")
        disc_data = json.loads(clean)
        # rip_data = data["rip_data"]

        return HTMLSystem.part(
            "pages/ripper/disc",
            DBID=db_id,
            DISCNAME=disc_data["disc_info"]["Name"],
            DISCLANGUAGE=disc_data["disc_info"]["MetadataLanguageName"],
            ISOFILE=data["iso_file"],
            UUID=data["uuid"].upper(),
            LABEL=data["label"],
            DISCTYPE=data["disc_type"].upper(),
            # DISCDATAJSON=data["disc_data"],
            # RIPDATAJSON=data["rip_data"]
        )

    def drives_data(self):
        """returns the group of drives html"""
        html = ""
        for drive_index, drive_obj in enumerate(Ripper.drives):
            html += HTMLSystem.part(
                "partial/ripper/drive",
                DRIVENUMBER=str(drive_index),
                NAME=drive_obj.name,
            )
        return html
