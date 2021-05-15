"""Ripper Root pages"""
import cherrypy

from data.disc_type import make_disc_type
from data.disc_type.base import DiscType
from database.ripper.video_info import RipperVideoInfo
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
        """Disc Edit Page"""
        info = RipperVideoInfo.get_or_none(RipperVideoInfo.id == db_id)
        if info is None:
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

        if not info.rip_data or info.rip_data == {}:
            return return_dict

        rip_data = make_disc_type(info.rip_data)
        return_dict["disc_items"] = rip_data.html_create_data(bool(info.rip_data_locked))
        return_dict["rip_data"] = rip_data.html_show_data(bool(info.rip_data_locked))

        return return_dict

    @cherrypy.tools.template(user=Auth.USER)
    def discs(self) -> dict:
        """Disc list Page"""
        data = []

        for item in RipperVideoInfo.do_select():

            data.append(
                {
                    "id": item.id,
                    "name": item.rip_data.get("name", item.label),
                    "disc_type": item.disc_type.upper(),
                    "type": item.rip_data.get("type", ""),
                    "rip_data": bool(item.rip_data),
                    "locked": bool(item.rip_data_locked),
                    "downloaded": bool(item.rip_data_downloaded),
                    "track_count": len(item.disc_data.get("track_info", [])),
                }
            )

        return {"data": data}
