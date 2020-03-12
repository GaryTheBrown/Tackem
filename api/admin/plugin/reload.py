'''PLUGIN RELOAD API'''
import cherrypy
from api.admin.plugin.base import APIPluginBase


@cherrypy.expose
class APIPluginReload(APIPluginBase):
    '''PLUGIN RELOAD API'''


    def POST(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        plugin_type = kwargs.get("plugin_type", None)
        plugin_name = kwargs.get("plugin_name", None)

        if self._system.is_plugin_loaded(plugin_type, plugin_name):
            return self._return_data_plugin(
                user,
                "Reload",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(),
                error=plugin_type + " " + plugin_name + " Already Reloaded",
                error_number=4
            )
        return_data = self._system.reload_plugin(plugin_type, plugin_name)
        if return_data[0] is not True:
            return self._return_data_plugin(
                user,
                "Reload",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(),
                error=return_data[0],
                error_number=return_data[1]
            )


        if self._system.load_plugin_systems(plugin_type, plugin_name) is not True:
            return self._return_data_plugin(
                user,
                "Reload",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(),
                error="Plugin Failed to load",
                error_number=5
            )

        return self._return_data_plugin(
            user,
            "Reload",
            True,
            plugin_type,
            plugin_name,
            actions=self._actions_return(
                [],  # enable
                [],  # disable
                [],  # show
                [],  # hide
                {},  # rename
            ),
        )
