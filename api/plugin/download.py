'''PLUGIN DOWNLOAD API'''

import cherrypy
from .base import APIPluginBase


@cherrypy.expose
class APIPluginDownload(APIPluginBase):
    '''PLUGIN DOWNLOAD API'''

    def GET(self, **kwargs) -> str:  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        raise cherrypy.HTTPError(status=404)


    def POST(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''POST Function'''
        raise cherrypy.HTTPError(status=404)


    def PUT(self, **kwargs) -> str: # pylint: disable=invalid-name,no-self-use
        '''PUT Function'''
        raise cherrypy.HTTPError(status=404)

    def download_plugin(self, **kwargs) -> str:
        '''The Action'''
        user = kwargs.get("user", self.GUEST)
        plugin_type = kwargs.get("plugin_type", None)
        plugin_name = kwargs.get("plugin_name", None)

        return_data = self._system.download_plugin(plugin_type, plugin_name)
        if return_data is not True:
            self._return_data_plugin(user, "Download", plugin_type, plugin_name, error=return_data)
        self._system.install_plugin_modules(plugin_type, plugin_name)
        return_data = self._system.reload_plugin(plugin_type, plugin_name)
        if return_data is not True:
            self._return_data_plugin(user, "Download", plugin_type, plugin_name, error=return_data)
