"""Base Template For the API"""
import cherrypy

from api.base import APIBase


@cherrypy.expose
class APIRipperDiscSave(APIBase):
    """Base Template For the API"""

    def POST(self, disc_id: int, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """POST Function"""

        return self._return_data("Ripper", f"Save Disc - {disc_id}", True, lockable=True)
