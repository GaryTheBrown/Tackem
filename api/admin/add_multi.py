'''Add Multi API'''
import cherrypy
from api.base import APIBase
from config_data import CONFIG


@cherrypy.expose
class APIAdminAddMulti(APIBase):
    '''Add Multi API'''

    def POST(self, **kwargs) -> str:
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        body = self._get_request_body()

        required = []
        if (plugin_type := body.get("plugin_type", None)) is None:
            required.append("plugin_type")
        if (plugin_name := body.get("plugin_name", None)) is None:
            required.append("plugin_name")
        if (instance_name := body.get("instance_name", None)) is None:
            required.append("instance_name")
        if required:
            return self._return_data(
                user,
                "addMulti",
                "Adding Instance of {} - {}".format(plugin_type, plugin_name),
                False,
                instance_name=instance_name,
                error="Missing Data Passed. Requires {}".format(", ".join(required)),
                errorNumber=0
            )

        var = instance_name.lower().replace(" ", "")
        if var in CONFIG["plugins"][plugin_type][plugin_name].keys():
            return self._return_data(
                user,
                "addMulti",
                "Adding Instance of {} - {}".format(plugin_type, plugin_name),
                False,
                instance_name=instance_name,
                error="Instance already exists",
                errorNumber=1
            )

        if not CONFIG["plugins"][plugin_type][plugin_name].clone_many_section(instance_name):
            return self._return_data(
                user,
                "addMulti",
                "Adding Instance of {} - {}".format(plugin_type, plugin_name),
                False,
                instance_name=instance_name,
                error="CLoning Data Failed",
                errorNumber=2
            )

        variable_name = "plugins_{}_{}_{}".format(plugin_type, plugin_name, instance_name)
        return self._return_data(
            user,
            "config",
            "Adding Instance of {} - {}".format(plugin_type, plugin_name),
            True,
            instance_name=instance_name,
            html=CONFIG["plugins"][plugin_type][plugin_name][instance_name].panel(variable_name)
        )
