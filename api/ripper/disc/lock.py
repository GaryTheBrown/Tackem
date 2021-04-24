"""Base Template For the API"""
import cherrypy
from peewee import DoesNotExist

from api.base import APIBase
from database.ripper.video_info import RipperVideoInfo


@cherrypy.expose
class APIRipperDiscLock(APIBase):
    """Base Template For the API"""

    def POST(self, disc_id: int, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """POST Function"""
        try:
            info = RipperVideoInfo.get_by_id(disc_id)
        except DoesNotExist:
            return self._return_data(
                "Ripper",
                f"Lock Disc - {disc_id}",
                False,
                error="Disc ID not in DB",
                errorNumber=0,
                lockable=False,
            )
        info: RipperVideoInfo = RipperVideoInfo.get_by_id(disc_id)

        if not info.rip_data or info.rip_data == {}:
            return self._return_data(
                "Ripper",
                f"Lock Disc - {disc_id}",
                False,
                error="Disc Rip data not Complete",
                errorNumber=1,
                lockable=False,
            )

        info.rip_data_locked = 1
        info.save()

        return self._return_data("Ripper", f"Lock Disc - {disc_id}", True, lockable=True)
