'''WebUI Config'''
import os
from libs.config.list import ConfigList
from libs.config.obj.integer_number import ConfigObjIntegerNumber
from libs.config.obj.string import ConfigObjString
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.option import ConfigObjOption
from libs.config.obj.options.select import ConfigObjOptionsSelect
from libs.startup_arguments import THEMEFOLDERLOCATION

def webui_config() -> ConfigList:
    '''WebUI Config'''
    return ConfigList(
        "webui",
        "Web Interface",
        ConfigObjIntegerNumber(
            "port",
            8081,
            "Port",
            "The port the system is accessed on",
            input_attributes=InputAttributes(
                min=1001,
                max=65535
            )
        ),
        ConfigObjString(
            "baseurl",
            "/",
            "Base Url",
            "The Base Url must start and end with '/'"
        ),
        ConfigObjOptionsSelect(
            "theme",
            [ConfigObjOption(x, x) for x in next(os.walk(THEMEFOLDERLOCATION))[1]],
            "default",
            "Theme",
            "The Theme for the system"
        )
    )
