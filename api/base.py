'''Base Template For the API'''
import json
import cherrypy


class APIBase():
    '''Base Template For the API'''


    GUEST = 0
    MASTER = 1
    USER = 2
    PLUGIN = 3


    def GET(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        raise cherrypy.HTTPError(status=404)


    def POST(self, **kwargs): # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        raise cherrypy.HTTPError(status=404)


    def PUT(self, **kwargs): # pylint: disable=invalid-name,no-self-use
        '''PUT Function'''
        raise cherrypy.HTTPError(status=404)


    def DELETE(self, **kwargs): # pylint: disable=invalid-name,no-self-use
        '''DELETE Function'''
        raise cherrypy.HTTPError(status=404)


    def _get_request_body(self):
        '''gets the requests body and returns dict'''
        content_length = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(content_length))
        return json.loads(rawbody)
