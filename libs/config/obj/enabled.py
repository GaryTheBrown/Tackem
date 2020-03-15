'''Config Object Boolean'''
from libs.config.obj.boolean import ConfigObjBoolean

class ConfigObjEnabled(ConfigObjBoolean):
    '''Config Item Boolean'''

    def __init__(self):
        super().__init__(
            "enabled",
            False,
            "Enabled",
            ""
        )
