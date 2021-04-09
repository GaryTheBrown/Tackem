"""Base Template For the API"""
import cherrypy

from api.base import APIBase
from data.disc_type import make_blank_disc_type
from data.video_track_type import VideoTrackType


@cherrypy.expose
class APIRipperDiscBlank(APIBase):
    """Base Template For the API"""

    def GET(self, disc_type: str, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""

        disc = make_blank_disc_type(disc_type)
        disc_data = disc.html_search_data()
        disc_html = cherrypy.tools.template.part("part/ripper/disc/disc_info", **disc_data)

        track_data = {
            "data_track_types_and_icons": VideoTrackType.TYPESANDICONS,
        }
        track_html = cherrypy.tools.template.part(
            "part/ripper/disc/track_type_select", **track_data
        )
        return self._return_data(
            "Ripper",
            f"Make Disc - {disc_type.capitalize()}",
            True,
            disc_html=disc_html,
            track_html=track_html,
        )
