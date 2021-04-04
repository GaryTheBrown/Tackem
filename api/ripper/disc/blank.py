"""Base Template For the API"""
import cherrypy

from api.base import APIBase
from data.disc_type import make_blank_disc_type


@cherrypy.expose
class APIRipperDiscBlank(APIBase):
    """Base Template For the API"""

    def GET(self, disc_type: str, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""

        disc = make_blank_disc_type(disc_type)
        html_data = disc.html_data()
        html = cherrypy.tools.template.part("part/ripper/disc/disc_info", **html_data)
        return self._return_data(
            cherrypy.request.params["user"],
            "Ripper",
            f"Make Disc - {disc_type.capitalize()}",
            True,
            disc_html=html,
        )
