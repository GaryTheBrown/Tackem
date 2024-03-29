"""WebUI Config"""
from config.backend.list import ConfigList
from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.obj.integer_number import ConfigObjIntegerNumber
from config.backend.obj.string import ConfigObjString


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
        ConfigObjString("socket", "0.0.0.0", "Host Socket", "The Host Socket 0.0.0.0 for all"),
        ConfigObjString("baseurl", "/", "Base Url", "The Base Url must start and end with '/'"),
        ConfigObjString(
            "uploadlocation",
            "upload/",
            "Temp Upload Location",
            "Location for temp storage of uploaded files",
        ),
    )
