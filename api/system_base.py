'''Base Template For the System API'''
import json
from .base import APIBase


class APISystemBase(APIBase):
    '''Base Template For the System API'''

    def __init__(self, system):
        self._system = system


    def GET(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        return json.dumps({"INPLUGIN": self._system.plugin_full_name})
