'''PLUGIN CLEAR CONFIG API'''
import shutil
from datetime import datetime
import cherrypy
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from config_data import CONFIG
from api.plugin.base import APIPluginBase


@cherrypy.expose
class APIPluginClearConfig(APIPluginBase):
    '''PLUGIN CLEAR CONFIG API'''

    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        return self.__clear_config_plugin(**kwargs)


    def POST(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        return self.__clear_config_plugin(**kwargs)


    def PUT(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''PUT Function'''
        return self.__clear_config_plugin(**kwargs)

    def __clear_config_plugin(self, **kwargs) -> str:
        '''The Action'''
        user = kwargs.get("user", self.GUEST)
        plugin_type = kwargs.get("plugin_type", None)
        plugin_name = kwargs.get("plugin_name", None)
        backup = kwargs.get("backup", True)

        if self._system.is_plugin_loaded(plugin_type, plugin_name):
            return self._return_data_plugin(
                user,
                "ClearConfig",
                False,
                plugin_type,
                plugin_name,
                actions=self._actions_return(),
                error=plugin_type + " " + plugin_name + " Has No Config Data",
                error_number=0
            )

        if not CONFIG['plugins'][plugin_type][plugin_name]:
            return

        config_file = PROGRAMCONFIGLOCATION + "config.ini"
        if backup:
            config_backup = PROGRAMCONFIGLOCATION + "config.bak"
            config_backup += datetime.now().strftime("%Y%m%d%H%M%S")
            shutil.copyfile(config_file, config_backup)
        CONFIG['plugins'][plugin_type][plugin_name].clear()
        CONFIG['plugins'][plugin_type].delete(plugin_name)
        if CONFIG['plugins'][plugin_type].count == 0:
            CONFIG['plugins'].delete(plugin_type)
        CONFIG.save()

        return self._return_data_plugin(
            user,
            "ClearConfig",
            True,
            plugin_type,
            plugin_name,
            actions=self._actions_return(),
        )
