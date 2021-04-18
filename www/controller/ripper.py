"""Ripper Root pages"""
import json

import cherrypy
from peewee import DoesNotExist

from data.disc_type import make_disc_type
from data.disc_type.base import DiscType
from database.ripper.video_info import VideoInfo
from libs import lower_keys
from libs.auth import Auth
from ripper import Ripper as RipperSYS


class Ripper:
    """ROOT OF PLUGINS WEBUI HERE"""

    @cherrypy.tools.template(user=Auth.USER)
    def index(self):
        """Index Page"""
        return {
            "drives": [drive.html_data(index) for index, drive in enumerate(RipperSYS.drives)],
            "isos": [iso.html_data() for iso in RipperSYS.isos],
            "isolimit": RipperSYS.maxisos,
            "videoconverters": [con.api_data() for con in RipperSYS.video_converters],
            "videoconverterlimit": RipperSYS.maxvideoconverters,
        }

    @cherrypy.tools.template(user=Auth.USER)
    def disc(self, db_id: int) -> dict:
        """Index Page"""
        try:
            info = VideoInfo.do_select().where(VideoInfo.id == db_id).get()
        except DoesNotExist:
            raise cherrypy.HTTPError(status=404)

        disc_data = lower_keys(info.disc_data)

        return_dict = {
            "db_id": db_id,
            "disc_name": disc_data["disc_info"]["name"],
            "disc_language": disc_data["disc_info"]["metadatalanguagename"],
            "iso_file": info.iso_file,
            "uuid": info.uuid.upper(),
            "label": info.label,
            "disc_type": info.disc_type.upper(),
            "disc_data": disc_data,
            "rip_data_locked": bool(info.rip_data_locked),
            "data_disc_types_and_icons": DiscType.TYPESANDICONS,
        }
        if not info.rip_data:
            return return_dict

        rip_data = make_disc_type(info.rip_data)
        return_dict["rip_data"] = json.loads(rip_data.html_data())
