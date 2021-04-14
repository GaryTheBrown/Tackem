"""Base Template For the API"""
import cherrypy

from api.base import APIBase
from data.video_track_type import make_blank_track_type


@cherrypy.expose
class APIRipperTrackBlank(APIBase):
    """Base Template For the API"""

    def GET(
        self, track_id: int, track_type: str, **kwargs
    ):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""

        track = make_blank_track_type(track_type)
        track_data = track.html_create_data(track_id)
        track_html = cherrypy.tools.template.part("part/ripper/disc/track_info", **track_data)

        return self._return_data(
            "Ripper",
            f"Make Track - {track_type.capitalize()}",
            True,
            track_html=track_html,
        )
