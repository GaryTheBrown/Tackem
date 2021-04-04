"""Base Template For the API"""
import cherrypy

from api.base import APIBase
from data.disc_type import DiscType


@cherrypy.expose
class APIRipperDiscDiscTypeSelect(APIBase):
    """Base Template For the API"""

    def GET(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""
        html_data = {
            "data_disc_types_and_icons": DiscType.TYPESANDICONS,
        }

        html = cherrypy.tools.template.part("part/ripper/disc/disc_type_select", **html_data)
        return self._return_data(
            cherrypy.request.params["user"],
            "Ripper",
            "Reset Make Disc",
            True,
            disc_html=html,
        )
