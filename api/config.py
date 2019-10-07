'''ROOT API'''
import json
import cherrypy
from system.full import TackemSystemFull
from .base import APIBase


@cherrypy.expose
class APIConfig(APIBase):
    '''CONFIG API'''


    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''
        location = []
        while vpath:
            location.append(vpath.pop(0))
        cherrypy.request.params['location'] = location
        return self


    def GET(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        user = kwargs.get("user", self.GUEST)
        location = kwargs.get("location", None)
        self._check_user(user)
        self.__check_for_blocked_locations(location)
        value = self.__check_location(location)

        return json.dumps({
            "system" : "config",
            "action" : "Get Config Option",
            "user" : user,
            "location": location,
            "setting": value
        })


    def POST(self, **kwargs):
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        location = kwargs.get("location", None)
        body = self._get_request_body()
        self._check_user(user)
        self.__check_for_blocked_locations(location)
        value = self.__check_location(location)
        self._tackem_system.set_config(location, body['value'])

        return json.dumps({
            "system" : "config",
            "action" : "Set Config Option",
            "user" : user,
            "location": location,
            "before": value,
            "after": body['value']
        })


    def __check_location(self, location):
        '''checks the location exists in the config and returns the value'''
        if location is None:
            raise cherrypy.HTTPError(status=400)  #Bad Request
        found, value = TackemSystemFull().get_config(location, None)
        if found is False:
            raise cherrypy.HTTPError(status=400)  #Bad Request
        return value


    def __check_for_blocked_locations(self, location):
        '''checks for banned locations'''
        if "masterkey" in location or "userkey" in location or location[0] == "plugins" \
            or location[0] == "systems":
            raise cherrypy.HTTPError(status=401)  #Unauthorized
