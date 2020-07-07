'''Delete Multi API'''
import cherrypy
from api.base import APIBase
from config_data import CONFIG

@cherrypy.expose
class APIAdminDeleteMulti(APIBase):
    '''Delete Multi API'''

    def POST(self, **kwargs) -> str:
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        required = []
        if (plugin_type:= kwargs.get("plugin_type", "")) == "":
            required.append("plugin_type")
        if (plugin_name:= kwargs.get("plugin_name", "")) == "":
            required.append("plugin_name")
        if (instance:= kwargs.get("instance", "")) == "":
            required.append("instance")
        if required:
            return self._return_data(
                user,
                "deleteMulti",
                "Adding Instance of {} - {}".format(plugin_type, plugin_name),
                False,
                instance=instance,
                error="Missing Data Passed. Requires {}".format(
                    ", ".join(required)),
                errorNumber=0
            )

        var = instance.lower().replace(" ", "")
        if not var in CONFIG["plugins"][plugin_type][plugin_name].keys():
            return self._return_data(
                user,
                "deleteMulti",
                "Adding Instance of {} - {}".format(plugin_type, plugin_name),
                False,
                instance=instance,
                error="Instance doesn't exists",
                errorNumber=1
            )

        if not CONFIG["plugins"][plugin_type][plugin_name].delete(instance):
            return self._return_data(
                user,
                "deleteMulti",
                "Adding Instance of {} - {}".format(plugin_type, plugin_name),
                False,
                instance=instance,
                error="Cloning Data Failed",
                errorNumber=2
            )

        return self._return_data(
            user,
            "config",
            "Adding Instance of {} - {}".format(plugin_type, plugin_name),
            True,
            instance=instance
        )
