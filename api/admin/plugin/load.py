'''PLUGIN LOAD API'''
import os
import cherrypy
from api.admin.plugin.base import APIPluginBase

@cherrypy.expose
class APIPluginLoad(APIPluginBase):
    '''PLUGIN LOAD API'''

    __INDOCKER = "You are running inside a docker container you need to pick an image that contains"
    __INDOCKER += " the required programs for the plugin"
    __EXTRA = "This Plugin Requires extra Programs Please see the readme"

    def POST(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        plugin_type = kwargs.get("plugin_type", None)
        plugin_name = kwargs.get("plugin_name", None)

        if self._system.is_plugin_loaded(plugin_type, plugin_name):
            return self._return_data_plugin(
                user,
                "Load",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(enable=["load"]),
                error="{} {} Already Loaded".format(plugin_type, plugin_name),
                error_number=0
            )

        if not self._system.load_plugin(plugin_type, plugin_name):
            if os.path.isfile("/indocker"):
                message = self.__INDOCKER
            else:
                message = self.__EXTRA
            return self._return_data_plugin(
                user,
                "Load",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(enable=["load"]),
                error="{} {} Failed to Load".format(plugin_type, plugin_name),
                error_number=1,
                message=message
            )
        return self._return_data_plugin(
            user,
            "Download",
            True,
            plugin_type,
            plugin_name,
            actions=self._actions_return(enable=["unload"]),
        )
