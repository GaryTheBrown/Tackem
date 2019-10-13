'''PLUGIN BASE API'''
from system.plugin_downloader import TackemSystemPluginDownloader
from ..base import APIBase

class APIPluginBase(APIBase):
    '''CONFIG API'''


    def __init__(self):
        self._system = TackemSystemPluginDownloader()

    @staticmethod
    def _plugin_page_data_return(enable: list, disable: list, show: list, hide: list) -> str:
        '''Creates the PLugin data to return'''
        data = {
            'actions': {
                'enable': enable,
                'disable': disable,
                'show': show,
                'hide':hide
            }
        }

    @staticmethod
    def _return_data_plugin(
            user: int,
            action: str,
            plugin_type: str,
            plugin_name: str,
            **kwargs
    ) -> str:
        '''creates the json for returning requiring some data but allowing more'''
        return APIBase._return_data(
            user,
            "Plugin",
            action,
            plugin_type=plugin_type,
            plugin_name=plugin_name,
            **kwargs
        )
