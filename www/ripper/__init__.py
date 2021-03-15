"""Ripper Root pages"""
import cherrypy

from data.config import CONFIG
from libs.authenticator import Authentication
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE
from libs.ripper import Ripper
from www.partial.uploads import PartialsUpload


class RipperRoot(HTMLTEMPLATE):
    """ROOT OF PLUGINS WEBUI HERE"""

    @cherrypy.expose
    def index(self):
        """index of Ripper"""
        Authentication.check_auth()
        return self._template(
            HTMLSystem.part(
                "pages/ripper/index",
                DRIVES=self.drives_data(),
                VIDEOUPLOADPARTIAL=PartialsUpload.video_iso(),
                AUDIOUPLOADPARTIAL=PartialsUpload.audio_iso(),
                ISOCOUNT=len(Ripper.isos),
                ISOTHREADLIMIT=CONFIG["ripper"]["iso"]["threadcount"].value,
                ISOTEMPLATE=HTMLSystem.open("partial/ripper/iso"),
            ),
            javascript=["js/ripper.js", "js/partial/ripperupload.js"],
        )

    def drives_data(self):
        """returns the group of drives html"""
        html = ""
        for drive_index, drive_obj in enumerate(Ripper.drives):
            html += HTMLSystem.part(
                "partial/ripper/drive",
                DRIVENUMBER=str(drive_index),
                NAME=drive_obj.name,
            )
        return html
