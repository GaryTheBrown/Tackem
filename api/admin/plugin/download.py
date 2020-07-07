'''PLUGIN DOWNLOAD API'''
import cherrypy
from api.admin.plugin.base import APIPluginBase

@cherrypy.expose
class APIPluginDownload(APIPluginBase):
    '''PLUGIN DOWNLOAD API'''

    def POST(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
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
        return_data = self._system.download_plugin(
            plugin_type.lower(), plugin_name.lower()
        )

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

        return self._return_data_plugin(
            user,
            "Download",
            True,
            plugin_type,
            plugin_name,
            actions=self._actions_return(
                enable=["load"]),
        )
