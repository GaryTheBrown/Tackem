'''Base Template For the API'''
from libs.ripper import Ripper
import cherrypy
from api.base import APIBase

@cherrypy.expose
class APIRipperISOData(APIBase):
    '''Base Template For the API'''

    def GET(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        user = kwargs.get("user", self.GUEST)
        if user == self.GUEST:
            raise cherrypy.HTTPError(status=403)
        try:
            index = int(kwargs.get("id", None))
        except ValueError:
            raise cherrypy.HTTPError(status=400)

        drives = Ripper.drives
        if index > len(drives):
            self._return()
        drive_dict = drives[index].api_data()
        return self._return_data(
            user,
            "Ripper",
            "Upload Video ISO",
            True,
            **drive_dict
        )
