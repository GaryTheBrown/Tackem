'''PLUGIN STOP API'''

import cherrypy
from api.admin.plugin.base import APIPluginBase


@cherrypy.expose
class APIPluginStop(APIPluginBase):
    '''PLUGIN STOP API'''

    def POST(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        plugin_type = kwargs.get("plugin_type", None)
        plugin_name = kwargs.get("plugin_name", None)

        if not self._system.is_plugin_loaded(plugin_type, plugin_name):
            return self._return_data_plugin(
                user,
                "Stop",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(),
                error=plugin_type + " " + plugin_name + " Not Running",
                error_number=0
            )

        self._system.stop_plugin_systems(plugin_type, plugin_name)
        return self._return_data_plugin(
            user,
            "Stop",
            True,
            plugin_type,
            plugin_name,
            actions=self._actions_return(),
        )
