'''RIPPER ISOS API'''
import cherrypy
from api.base import APIBase
from data.config import CONFIG

@cherrypy.expose
class APIRipperIsos(APIBase):
    '''Ripper ISOS API'''

    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''

        if not CONFIG['ripper']['isos']['enabled'].value or len(vpath) == 0:
            return self

        # section = vpath.pop(0)

        # if section == "uploadaudio":
            # return API()
        # if section == "uploadvideo":
            # return API()
        return self
