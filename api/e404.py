"""Base Template For the API"""
import cherrypy


class API404:
    """Base Template For the API"""

    def GET(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """GET Function"""
        raise cherrypy.HTTPError(status=404)

    def POST(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """POST Function"""
        raise cherrypy.HTTPError(status=404)

    def PUT(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """PUT Function"""
        raise cherrypy.HTTPError(status=404)

    def DELETE(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """DELETE Function"""
        raise cherrypy.HTTPError(status=404)
