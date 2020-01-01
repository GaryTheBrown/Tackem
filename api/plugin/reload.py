'''PLUGIN RELOAD API'''
import cherrypy
from api.plugin.base import APIPluginBase


@cherrypy.expose
class APIPluginReload(APIPluginBase):
    '''PLUGIN RELOAD API'''

    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        return self.__reload_plugin(**kwargs)


    def POST(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        return self.__reload_plugin(**kwargs)


    def PUT(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''PUT Function'''
        return self.__reload_plugin(**kwargs)

    def __reload_plugin(self, **kwargs) -> str:
        '''The Action'''
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
                actions=self._actions_return(
                    [],  # enable
                    [],  # disable
                    [],  # show
                    [],  # hide
                    {},  # rename
                ),
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
                actions=self._actions_return(
                    [],  # enable
                    [],  # disable
                    [],  # show
                    [],  # hide
                    {},  # rename
                ),
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
                actions=self._actions_return(
                    [],  # enable
                    [],  # disable
                    [],  # show
                    [],  # hide
                    {},  # rename
                ),
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
