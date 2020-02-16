'''PLUGIN START API'''

import cherrypy
from api.plugin.base import APIPluginBase


@cherrypy.expose
class APIPluginStart(APIPluginBase):
    '''PLUGIN START API'''

    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        return self.__start_plugin(**kwargs)


    def POST(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        return self.__start_plugin(**kwargs)


    def PUT(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''PUT Function'''
        return self.__start_plugin(**kwargs)

    def __start_plugin(self, **kwargs) -> str:
        '''The Action'''
        user = kwargs.get("user", self.GUEST)
        plugin_type = kwargs.get("plugin_type", None)
        plugin_name = kwargs.get("plugin_name", None)

        if self._system.is_plugin_loaded(plugin_type, plugin_name):
            return self._return_data_plugin(
                user,
                "Start",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(),
                error=plugin_type + " " + plugin_name + " Already Started",
                error_number=0
            )
        if not self._system.load_plugin_systems(plugin_type, plugin_name):
            return self._return_data_plugin(
                user,
                "Start",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(),
                error=plugin_type + " " + plugin_name + " Failed to Started",
                error_number=1
            )
        return self._return_data_plugin(
            user,
            "Download",
            True,
            plugin_type,
            plugin_name,
            actions=self._actions_return(),
        )
