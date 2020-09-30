'''PLUGIN UNLOAD API'''
import cherrypy
from api.admin.plugin.base import APIPluginBase

@cherrypy.expose
class APIPluginUnload(APIPluginBase):
    '''PLUGIN UNLOAD API'''

    def POST(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        plugin_type = kwargs.get("plugin_type", None)
        plugin_name = kwargs.get("plugin_name", None)

        if not self._system.is_plugin_loaded(plugin_type, plugin_name):
            return self._return_data_plugin(
                user,
                "Unload",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(enable=["unload"]),
                error="{} {} Not Loaded".format(plugin_type, plugin_name),
                error_number=0
            )
        if self._system.is_systems_for_plugin_running(plugin_type, plugin_name):
            self._system.stop_plugin_systems(plugin_type, plugin_name)

        if self._system.do_systems_for_plugin_exist(plugin_type, plugin_name):
            self._system.unload_plugin_systems(plugin_type, plugin_name)

        self._system.unload_plugin(plugin_type, plugin_name)

        return self._return_data_plugin(
            user,
            "Unload",
            True,
            plugin_type,
            plugin_name,
            actions=self._actions_return(enable=["load", "delete"]),
        )
