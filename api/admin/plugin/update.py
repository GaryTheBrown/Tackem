'''PLUGIN UPDATE API'''
import cherrypy
from api.admin.plugin.base import APIPluginBase

@cherrypy.expose
class APIPluginUpdate(APIPluginBase):
    '''PLUGIN UPDATE API'''

    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        return self.__update_plugin(**kwargs)


    def POST(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        return self.__update_plugin(**kwargs)


    def PUT(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''PUT Function'''
        return self.__update_plugin(**kwargs)

    def __update_plugin(self, **kwargs) -> str:
        '''The Action'''
        user = kwargs.get("user", self.GUEST)
        plugin_type = kwargs.get("plugin_type", None)
        plugin_name = kwargs.get("plugin_name", None)

        if self._system.is_plugin_loaded(plugin_type, plugin_name):
            return self._return_data_plugin(
                user,
                "Update",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(),
                error=plugin_type + " " + plugin_name + "Is Running. Stop it First",
                error_number=0
            )

        if not self._system.update_plugin(plugin_type, plugin_name):
            return self._return_data_plugin(
                user,
                "Update",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(),
                error=plugin_type + " " + plugin_name + " Failed to Update",
                error_number=1
            )

        return self._return_data_plugin(
            user,
            "Update",
            True,
            plugin_type,
            plugin_name,
            actions=self._actions_return(),
        )
