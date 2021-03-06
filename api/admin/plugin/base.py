'''PLUGIN BASE API'''
from system.plugin_downloader import TackemSystemPluginDownloader
from api.base import APIBase

class APIPluginBase(APIBase):
    '''PLUGIN BASE API'''

    def __init__(self):
        self._system = TackemSystemPluginDownloader()

    def _return_data_plugin(
            self,
            user: int,
            action: str,
            success: bool,
            plugin_type: str,
            plugin_name: str,
            **kwargs
    ) -> str:
        '''creates the json for returning requiring some data but allowing more'''
        return self._return_data(
            user,
            "Plugin",
            action,
            success,
            plugin_type=plugin_type,
            plugin_name=plugin_name,
            **kwargs
        )
