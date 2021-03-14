'''RIPPER DRIVES API'''
from api.ripper.drives.data import APIRipperDrivesData
import cherrypy
from api.base import APIBase
from data.config import CONFIG


@cherrypy.expose
class APIRipperDrives(APIBase):
    '''Ripper Drives API'''

    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''

        if not CONFIG['ripper']['drives']['enabled'].value or len(vpath) == 0:
            return self

        section = vpath.pop(0)

        if section == "data":
            return APIRipperDrivesData()
        return self
