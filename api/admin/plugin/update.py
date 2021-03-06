'''PLUGIN UPDATE API'''
import cherrypy
from api.admin.plugin.base import APIPluginBase

@cherrypy.expose
class APIPluginUpdate(APIPluginBase):
    '''PLUGIN UPDATE API'''

    def POST(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        plugin_type = kwargs.get("plugin_type", None)
        plugin_name = kwargs.get("plugin_name", None)

        if not self._system.update_plugin(plugin_type, plugin_name):
            return self._return_data_plugin(
                user,
                "Update",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(enable=["load"]),
                error=f"{plugin_type} {plugin_name} Failed to Update",
                error_number=1
            )

        return self._return_data_plugin(
            user,
            "Update",
            True,
            plugin_type,
            plugin_name,
            actions=self._actions_return(enable=["load"]),
        )
