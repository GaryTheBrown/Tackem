"""CONFIG API"""
import cherrypy

from api.base import APIBase
from data.config import CONFIG


@cherrypy.expose
class APIAdminConfig(APIBase):
    """CONFIG API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""
        location = []
        while vpath:
            location.append(vpath.pop(0))
        cherrypy.request.params["location"] = location
        return self

    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        """GET Function"""
        user = kwargs.get("user", self.GUEST)
        location = kwargs.get("location", None)
        self._check_user(user)
        self.__check_for_blocked_locations(location)
        value = CONFIG.find_and_get(location)

        return self._return_data(
            user, "config", "Get CONFIG Option", True, location=location, setting=value
        )

    def POST(self, **kwargs) -> str:
        """POST Function"""
        user = kwargs.get("user", self.GUEST)
        location = kwargs.get("location", None)
        body = self._get_request_body()
        self._check_user(user)
        self.__check_for_blocked_locations(location)
        value = CONFIG.find_and_get(location)
        CONFIG.find_and_set(location, body["value"])

        return self._return_data(
            user,
            "config",
            "set CONFIG Option",
            True,
            location=location,
            before=value,
            after=body["value"],
        )

    def __check_for_blocked_locations(self, location: str):
        """checks for banned locations"""
        if (
            "masterkey" in location
            or "userkey" in location
            or location[0] == "plugins"
            or location[0] == "systems"
        ):
            raise cherrypy.HTTPError(status=401)  # Unauthorized
