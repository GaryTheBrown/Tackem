"""Base Template For the API"""
import cherrypy
from peewee import DoesNotExist

from api.base import APIBase
from data.disc_type import make_disc_type
from database.ripper.video_info import VideoInfo


@cherrypy.expose
class APIRipperDiscSave(APIBase):
    """Base Template For the API"""

    def POST(self, disc_id: int, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """POST Function"""
        data = {"tracks": []}
        for key, value in kwargs.items():
            if "_" not in key:
                continue
            if key == "disc_type":
                data["type"] = value

            s = key.split("_")
            if s[0] == "disc":
                data[s[1]] = value
                continue

            if s[0] == "track":
                if int(s[1]) > len(data["tracks"]):
                    data["tracks"].append({s[2]: value})
                else:
                    data["tracks"][int(s[1]) - 1][s[2]] = value
        disc = make_disc_type(data)

        try:
            info = VideoInfo.get_by_id(disc_id)
        except DoesNotExist:
            return self._return_data(
                "Ripper",
                f"Save Disc - {disc_id}",
                False,
                error="Disc ID not in DB",
                errorNumber=0,
                lockable=False,
            )

        if info.rip_data_locked:
            return self._return_data(
                "Ripper",
                f"Save Disc - {disc_id}",
                False,
                error="Disc ID Locked Cannot alter",
                errorNumber=1,
                lockable=False,
            )

        info.rip_data = disc.make_dict()
        info.save()

        return self._return_data(
            "Ripper",
            f"Save Disc - {disc_id}",
            True,
            lockable=True,
        )
