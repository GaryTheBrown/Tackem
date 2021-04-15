"""Base Template For the API"""
import cherrypy

from api.base import APIBase


@cherrypy.expose
class APIRipperDiscLock(APIBase):
    """Base Template For the API"""

    def POST(self, disc_id: int, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """POST Function"""

        return self._return_data("Ripper", f"Lock Disc - {disc_id}", True, recieved=kwargs)
