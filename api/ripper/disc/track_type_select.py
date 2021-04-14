"""Base Template For the API"""
import cherrypy

from api.base import APIBase
from data.disc_type import make_blank_disc_type


@cherrypy.expose
class APIRipperDiscTrackTypeSelect(APIBase):
    """Base Template For the API"""

    def GET(self, disc_type: str, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""

        disc = make_blank_disc_type(disc_type)

        track_data = {
            "data_track_types_and_icons": disc.track_types_and_icons,
        }
        track_html = cherrypy.tools.template.part(
            "part/ripper/disc/track_type_select", **track_data
        )
        return self._return_data("Ripper", "Reset Make Track", True, track_html=track_html)
