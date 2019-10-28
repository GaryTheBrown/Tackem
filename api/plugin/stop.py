'''PLUGIN STOP API'''

import cherrypy
from .base import APIPluginBase


@cherrypy.expose
class APIPluginStop(APIPluginBase):
    '''PLUGIN STOP API'''

    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        return self.__stop_plugin(**kwargs)


    def POST(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        return self.__stop_plugin(**kwargs)


    def PUT(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''PUT Function'''
        return self.__stop_plugin(**kwargs)

    def __stop_plugin(self, **kwargs) -> str:
        '''The Action'''
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
                actions=self._actions_return(
                    [],  # enable
                    [],  # disable
                    [],  # show
                    [],  # hide
                    {},  # rename
                ),
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
            actions=self._actions_return(
                [],  # enable
                [],  # disable
                [],  # show
                [],  # hide
                {},  # rename
            ),
        )
