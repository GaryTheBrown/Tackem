'''Add Multi API'''
import cherrypy
from api.base import APIBase
from data.config import CONFIG

@cherrypy.expose
class APIAdminAddMulti(APIBase):
    '''Add Multi API'''

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
                "addMulti",
                f"Adding Instance of {plugin_type} - {plugin_name}",
                False,
                instance=instance,
                error=f"Missing Data Passed. Requires {', '.join(required)}",
                errorNumber=0
            )

        var = instance.lower().replace(" ", "")
        if var in CONFIG["plugins"][plugin_type][plugin_name].keys():
            return self._return_data(
                user,
                "addMulti",
                f"Adding Instance of {plugin_type} - {plugin_name}",
                False,
                instance=instance,
                error="Instance already exists",
                errorNumber=1
            )

        if not CONFIG["plugins"][plugin_type][plugin_name].clone_many_section(instance):
            return self._return_data(
                user,
                "addMulti",
                f"Adding Instance of {plugin_type} - {plugin_name}",
                False,
                instance=instance,
                error="Cloning Data Failed",
                errorNumber=2
            )

        variable_name = f"plugins_{plugin_type}_{plugin_name}"
        return self._return_data(
            user,
            "config",
            f"Adding Instance of {plugin_type} - {plugin_name}",
            True,
            instance=instance,
            html=CONFIG["plugins"][plugin_type][plugin_name][instance].panel(
                variable_name,
                instance.title()
            )
        )
