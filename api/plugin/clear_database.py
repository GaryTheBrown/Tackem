'''PLUGIN CLEAR DATABASE API'''

import cherrypy
from .base import APIPluginBase


@cherrypy.expose
class APIPluginClearDatabase(APIPluginBase):
    '''PLUGIN CLEAR DATABASE API'''


    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        return self.__clear_database_plugin(**kwargs)


    def POST(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        return self.__clear_database_plugin(**kwargs)


    def PUT(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''PUT Function'''
        return self.__clear_database_plugin(**kwargs)


    def __clear_database_plugin(self, **kwargs) -> str:
        '''The Action'''
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
                actions=self._actions_return(
                    [],  # enable
                    [],  # disable
                    [],  # show
                    [],  # hide
                    {},  # rename
                ),
                error=plugin_type + " " + plugin_name + " Has No Database Data",
                error_number=0
            )

        name_like = plugin_type + "_" + plugin_name + "_%"
        results = self._system.sql.select_like(
            "api",
            "table_version",
            {'name':name_like}
        )
        for result in results:
            self._system.sql.call("api", "DROP TABLE " + result['name'] + ";")
            self._system.sql.delete_row("api", "table_version", result['id'])

        return self._return_data_plugin(
            user,
            "ClearDatabase",
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
