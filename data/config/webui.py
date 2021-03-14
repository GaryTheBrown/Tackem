"""WebUI Config"""
from libs.config.list import ConfigList
from libs.config.obj.integer_number import ConfigObjIntegerNumber
from libs.config.obj.string import ConfigObjString
from libs.config.obj.data.input_attributes import InputAttributes


def webui_config() -> ConfigList:
    """WebUI Config"""
    return ConfigList(
        "webui",
        "Web Interface",
        ConfigObjIntegerNumber(
            "port",
            8081,
            "Port",
            "The port the system is accessed on",
            input_attributes=InputAttributes(min=1001, max=65535),
        ),
        ConfigObjString(
            "baseurl", "/", "Base Url", "The Base Url must start and end with '/'"
        ),
        ConfigObjString(
            "uploadlocation",
            "upload/",
            "Temp Upload Location",
            "Location for temp storage of uploaded files",
        ),
    )
