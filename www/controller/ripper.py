"""Ripper Root pages"""
import json

import cherrypy

from data.database.ripper import VIDEO_INFO_DB
from data.disc_type import make_disc_type
from data.disc_type.base import DiscType
from libs import lower_keys
from libs.authentication import Authentication
from libs.database import Database
from libs.database.messages.select import SQLSelect
from libs.database.where import Where
from libs.ripper import Ripper as RipperSYS


class Ripper:
    """ROOT OF PLUGINS WEBUI HERE"""

    @cherrypy.tools.template(user=Authentication.USER)
    def index(self):
        """Index Page"""
        return {
            "drives": [drive.html_data(index) for index, drive in enumerate(RipperSYS.drives)],
            "isos": [iso.html_data() for iso in RipperSYS.isos],
            "isolimit": RipperSYS.maxisos,
            "videoconverters": [con.api_data() for con in RipperSYS.video_converters],
            "videoconverterlimit": RipperSYS.maxvideoconverters,
        }

    @cherrypy.tools.template(user=Authentication.USER)
    def disc(self, db_id: int) -> dict:
        """Index Page"""
        msg = SQLSelect(VIDEO_INFO_DB, Where("id", db_id))
        Database.call(msg)
        if isinstance(msg.return_data, list):
            raise cherrypy.HTTPError(status=404)

        clean_disc_data = msg.return_data["disc_data"].replace('\\"', "")
        disc_data = lower_keys(json.loads(clean_disc_data))

        return_dict = {
            "db_id": db_id,
            "disc_name": disc_data["disc_info"]["name"],
            "disc_language": disc_data["disc_info"]["metadatalanguagename"],
            "iso_file": msg.return_data["iso_file"],
            "uuid": msg.return_data["uuid"].upper(),
            "label": msg.return_data["label"],
            "disc_type": msg.return_data["disc_type"].upper(),
            "disc_data": disc_data,
            "rip_data_locked": bool(msg.return_data["rip_data_locked"]),
            "data_disc_types_and_icons": DiscType.TYPESANDICONS,
        }
        if not msg.return_data["rip_data"]:
            return return_dict

        rip_data = make_disc_type(msg.return_data["rip_data"].replace('\\"', ""))
        return_dict["rip_data"] = json.loads(rip_data.html_data())
