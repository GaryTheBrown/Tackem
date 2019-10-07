'''Base Template For the API'''
import json
import cherrypy
from system.full import TackemSystemFull


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


    def _check_api_key(self, key):
        '''checks the api key against the master and user keys and returns the level'''
        _, masterapi = TackemSystemFull().get_config(["masterapi", "key"], None)
        _, userapi = TackemSystemFull().get_config(["userapi", "key"], None)
        if key is None or not isinstance(key, str):
            return self.GUEST
        if key == "aaa": ## masterapi:
            return self.MASTER
        if key == "bbb": ## userapi:
            return self.USER
        if key == "ccc":
            return self.PLUGIN
        return self.GUEST


    def _check_session_id(self):
        '''checks the session Id is in the list'''
        if not TackemSystemFull().auth.check_logged_in():
            return self.GUEST
        if TackemSystemFull().auth.is_admin():
            return self.MASTER
        return self.USER


    def _check_user(self, user, is_admin=False):
        '''checks that the user is allowed'''
        if user == self.GUEST or (is_admin and user == self.USER):
            raise cherrypy.HTTPError(status=401)  #Unauthorized


    def _get_request_body(self):
        '''gets the requests body and returns dict'''
        content_length = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(content_length))
        return json.loads(rawbody)
