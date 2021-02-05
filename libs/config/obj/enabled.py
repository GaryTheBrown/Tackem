'''Config Object Boolean'''
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.boolean import ConfigObjBoolean

class ConfigObjEnabled(ConfigObjBoolean):
    '''Config Item Boolean'''

    def __init__(self, default_value=False, disabled=False):
        if disabled:
            super().__init__(
                "enabled",
                default_value,
                "Enabled",
                "",
                input_attributes=InputAttributes("disabled")
            )
        else:
            super().__init__(
                "enabled",
                default_value,
                "Enabled",
                ""
            )
