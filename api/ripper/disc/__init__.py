"""RIPPER DRIVES API"""
import cherrypy

from api.base import APIBase
from api.e404 import API404
from api.ripper.disc.blank_disc import APIRipperDiscBlank
from api.ripper.disc.blank_track import APIRipperTrackBlank
from api.ripper.disc.disc_type_select import APIRipperDiscDiscTypeSelect
from api.ripper.disc.lock import APIRipperDiscLock
from api.ripper.disc.save import APIRipperDiscSave
from api.ripper.disc.search_data import APIRipperDiscSearchData
from api.ripper.disc.track_type_select import APIRipperDiscTrackTypeSelect
from api.ripper.disc.upload import APIRipperDiscUpload


@cherrypy.expose
class APIRipperDisc(APIBase):
    """Ripper Drives API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""

        if len(vpath) == 0:
            return self
        section = vpath.pop(0).lower()
        if section == "blankdisc":
            return APIRipperDiscBlank()
        if section == "blanktrack":
            return APIRipperTrackBlank()
        if section == "disctypeselect":
            return APIRipperDiscDiscTypeSelect()
        if section == "tracktypeselect":
            return APIRipperDiscTrackTypeSelect()
        if section == "save":
            return APIRipperDiscSave()
        if section == "lock":
            return APIRipperDiscLock()
        if section == "upload":
            return APIRipperDiscUpload()
        if section == "searchapi":
            return APIRipperDiscSearchData()
        return API404()
