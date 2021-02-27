'''Upload Audio ISO API'''
import cherrypy
from api.base import APIBase

@cherrypy.expose
class APIRipperIsoUploadAudio(APIBase):
    '''Upload Audio ISO API'''

    def POST(self, **kwargs) -> str:
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
