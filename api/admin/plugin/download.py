'''PLUGIN DOWNLOAD API'''
import os
import cherrypy
from api.admin.plugin.base import APIPluginBase


@cherrypy.expose
class APIPluginDownload(APIPluginBase):
    '''PLUGIN DOWNLOAD API'''

    __INDOCKER = "You are running inside a docker container you need to pick an image that contains"
    __INDOCKER += " the required programs for the plugin"
    __EXTRA = "This Plugin Requires extra Programs Please see the readme"


    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        return self.__download_plugin(**kwargs)


    def POST(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        return self.__download_plugin(**kwargs)


    def PUT(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''PUT Function'''
        return self.__download_plugin(**kwargs)


    def __download_plugin(self, **kwargs) -> str:
        '''The Action'''
        user = kwargs.get("user", self.GUEST)
        plugin_type = kwargs.get("plugin_type", "").lower()
        plugin_name = kwargs.get("plugin_name", "").lower()

        if plugin_name == "" or plugin_type == "":
            return self._return_data_plugin(
                user,
                "Download",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(enable=["download"]),
                error="No Plugin Details Given",
                error_number=0
            )
        return_data = self._system.download_plugin(plugin_type.lower(), plugin_name.lower())
        if return_data[0] is not True:
            return self._return_data_plugin(
                user,
                "Download",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(enable=["download"]),
                error=return_data[0],
                error_number=return_data[1]
            )
        self._system.install_plugin_modules(plugin_type, plugin_name)
        return_data = self._system.reload_plugin(plugin_type, plugin_name)
        if return_data[0] is not True:
            if os.path.isfile("/indocker"):
                message = self.__INDOCKER
            else:
                message = self.__EXTRA

            return self._return_data_plugin(
                user,
                "Download",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(enable=["download"]),
                error=return_data[0],
                error_number=return_data[1],
                message=message
            )

        return self._return_data_plugin(
            user,
            "Download",
            True,
            plugin_type,
            plugin_name,
            actions=self._actions_return(enable=["start", "clearconfig", "cleardatabase"]),
        )
