"""Base Template For the API"""
import cherrypy
from peewee import DoesNotExist

from api.base import APIBase
from database.ripper.video_info import VideoInfo
from ripper.disc_api import DiscAPI


@cherrypy.expose
class APIRipperDiscSearchData(APIBase):
    """Base Template For the API"""

    def GET(self, disc_id: int, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""
        try:
            info = VideoInfo.get_by_id(disc_id)
        except DoesNotExist:
            return self._return_data(
                "Ripper",
                f"Search For Disc Data - {disc_id}",
                False,
                error="Disc ID not in DB",
                errorNumber=0,
            )
        info: VideoInfo = VideoInfo.get_by_id(disc_id)

        if info.rip_data and info.rip_data != {}:
            return self._return_data(
                "Ripper",
                f"Search For Disc Data - {disc_id}",
                False,
                error="Disc Rip data already Exists",
                errorNumber=1,
            )

        data = DiscAPI.find_disctype(info.uuid, info.label)

        if data:
            info.rip_data = data.make_dict()
            info.rip_data_downloaded = 1
            info.rip_data_locked = 1
            info.save()

        return self._return_data("Ripper", f"Lock Disc - {disc_id}", True, found=bool(data))
