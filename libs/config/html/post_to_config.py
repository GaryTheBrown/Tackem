'''Config File Setup'''
from typing import Any
from config_data import CONFIG
from libs.config.list import ConfigList
from libs.config.obj.enabled import ConfigObjEnabled
from libs.root_event import RootEvent

def post_config_settings(kwargs: Any):
    '''Fills in the config dict with the settings based on its name'''

    for key, value in kwargs.items():
        key = key.replace("[]", "")
        key_list = key.split("_")
        add_val_to_config(key, CONFIG, key_list, value)

def add_val_to_config(key: str, config: ConfigList, key_list: list, value: Any):
    '''recursive way of adding value into the config'''
    if len(key_list) == 1:
        if key_list[0] in config.keys():
            config_item = config[key_list[0]]
            if isinstance(config_item, ConfigObjEnabled) and "plugins" in key:
                if config_item.value != bool(int(value)):
                    system_key = " ".join(key.split("_")[1:-1])
                    if bool(int(value)):
                        print("START SYSTEM", system_key)
                        RootEvent.set_event("start_system", system_key)
                    else:
                        print("STOP SYSTEM", system_key)
                        RootEvent.set_event("stop_system", system_key)
            config_item.value = value
            return

        for obj in config:
            if isinstance(obj, ConfigList) and obj.is_section:
                if key_list[0] in obj.keys():
                    obj[key_list[0]].value = value
                    return
    else:
        if config.many_section:
            config.clone_many_section(key_list[0])

        if key_list[0] in config.keys():
            return add_val_to_config(key, config[key_list[0]], key_list[1:], value)

        for obj in config:
            if obj.is_section:
                return add_val_to_config(key, obj, key_list, value)
