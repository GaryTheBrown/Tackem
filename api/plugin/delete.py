'''PLUGIN DELETE API'''

import cherrypy
from api.plugin.base import APIPluginBase


@cherrypy.expose
class APIPluginDelete(APIPluginBase):
    '''PLUGIN DELETE API'''

    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        return self.__delete_plugin(**kwargs)


    def POST(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        return self.__delete_plugin(**kwargs)


    def PUT(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''PUT Function'''
        return self.__delete_plugin(**kwargs)

    def __delete_plugin(self, **kwargs) -> str:
        '''The Action'''
        user = kwargs.get("user", self.GUEST)
        plugin_type = kwargs.get("plugin_type", None)
        plugin_name = kwargs.get("plugin_name", None)

        loaded_data = self._system.is_plugin_loaded(plugin_type, plugin_name)
        if loaded_data is True:
            self._system.stop_plugin_systems(plugin_type, plugin_name)
            self._system.write_config_to_disk()
            self._system.remove_plugin(plugin_type, plugin_name)

        delete_data = self._system.delete_plugin(plugin_type, plugin_name)
        if delete_data[0] is not True:
            return self._return_data_plugin(
                user,
                "Delete",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(),
                error=delete_data[0],
                error_number=delete_data[1]
            )


        if loaded_data is True:
            self._system.remove_plugin_cfg(plugin_type, plugin_name)
            self._system.load_config()

        return self._return_data_plugin(
            user,
            "Delete",
            True,
            plugin_type,
            plugin_name,
            actions=self._actions_return(),
        )
