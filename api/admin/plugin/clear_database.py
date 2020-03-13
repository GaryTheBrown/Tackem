'''PLUGIN CLEAR DATABASE API'''

import cherrypy
from api.admin.plugin.base import APIPluginBase
from libs.sql import Database


@cherrypy.expose
class APIPluginClearDatabase(APIPluginBase):
    '''PLUGIN CLEAR DATABASE API'''

    def POST(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        plugin_type = kwargs.get("plugin_type", None)
        plugin_name = kwargs.get("plugin_name", None)

        if self._system.is_plugin_loaded(plugin_type, plugin_name):
            return self._return_data_plugin(
                user,
                "ClearDatabase",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(),
                error=plugin_type + " " + plugin_name + " Has No Database Data",
                error_number=0
            )

        name_like = plugin_type + "_" + plugin_name + "_%"
        results = Database.sql().select_like(
            "api",
            "table_version",
            {'name': name_like}
        )
        for result in results:
            Database.sql().call("api", "DROP TABLE " + result['name'] + ";")
            Database.sql().delete_row("api", "table_version", result['id'])

        return self._return_data_plugin(
            user,
            "ClearDatabase",
            True,
            plugin_type,
            plugin_name,
            actions=self._actions_return(),
        )
