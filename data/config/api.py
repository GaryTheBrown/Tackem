"""API Config"""
from libs.config.list import ConfigList
from libs.config.obj.data.button import Button
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.string import ConfigObjString


def api_config() -> ConfigList:
    """API Config"""
    return ConfigList(
        "api",
        "API Interface",
        ConfigObjString(
            "masterkey",
            "",
            "Master API Key",
            "The master API key for full control",
            button=Button("Generate API Key", "generateAPIKey", True, input="api_masterkey"),
            input_attributes=InputAttributes("readonly"),
        ),
        ConfigObjString(
            "userkey",
            "",
            "User API Key",
            "The user API key for limited control",
            button=Button("Generate API Key", "generateAPIKey", True, input="api_userkey"),
            input_attributes=InputAttributes("readonly"),
        ),
    )
