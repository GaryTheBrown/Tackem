'''PLUGIN DELETE API'''

import cherrypy
from api.admin.plugin.base import APIPluginBase
from config_data import CONFIG


@cherrypy.expose
class APIPluginDelete(APIPluginBase):
    '''PLUGIN DELETE API'''

    def POST(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        plugin_type = kwargs.get("plugin_type", None)
        plugin_name = kwargs.get("plugin_name", None)

        loaded_data = self._system.is_plugin_loaded(plugin_type, plugin_name)
        if loaded_data is True:
            self._system.stop_plugin_systems(plugin_type, plugin_name)
            CONFIG.save()
            self._system.remove_plugin(plugin_type, plugin_name)

        delete_data = self._system.delete_plugin(plugin_type, plugin_name)
        if delete_data[0] is not True:
            return self._return_data_plugin(
                user,
                "Delete",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(enable=["self"]),
                error=delete_data[0],
                error_number=delete_data[1]
            )

        if loaded_data is True:
            CONFIG['plugins'][plugin_type][plugin_name].clear()
            CONFIG['plugins'][plugin_type].delete(plugin_name)
            if CONFIG['plugins'][plugin_type].count == 0:
                CONFIG['plugins'].delete(plugin_type)
            CONFIG.load()

        return self._return_data_plugin(
            user,
            "Delete",
            True,
            plugin_type,
            plugin_name,
            actions=self._actions_return(enabled=["download"]),
        )
