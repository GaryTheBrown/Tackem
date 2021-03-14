"""RIPPER ISOS API"""
from api.ripper.iso.data import APIRipperISOData
from api.ripper.iso.upload_audio import APIRipperIsoUploadAudio
from api.ripper.iso.upload_video import APIRipperIsoUploadVideo
import cherrypy
from api.base import APIBase
from data.config import CONFIG


@cherrypy.expose
class APIRipperIsos(APIBase):
    """Ripper ISOS API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""

        if not CONFIG["ripper"]["iso"]["enabled"].value or len(vpath) == 0:
            return self

        section = vpath.pop(0)

        if section == "data":
            return APIRipperISOData()
        if section == "uploadaudio":
            return APIRipperIsoUploadAudio()
        if section == "uploadvideo":
            return APIRipperIsoUploadVideo()
        return self
