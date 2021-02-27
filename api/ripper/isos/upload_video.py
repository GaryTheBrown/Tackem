'''Upload Video ISO API'''
import cherrypy
from api.base import APIBase

@cherrypy.expose
class APIRipperIsoUploadVideo(APIBase):
    '''Upload Video ISO API'''

    def POST(self, **kwargs) -> str:
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        if "filename" not in kwargs:
            return self._return_data(
                user,
                "Ripper",
                "Upload Video ISO",
                False,
                error="Missing Filename",
                errorNumber=0
            )

        #TODO add into upload DB and return a KEY for the user.
