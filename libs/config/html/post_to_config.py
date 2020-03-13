'''Config File Setup'''
from config_data import CONFIG
from libs.config.list import ConfigList


def post_config_settings(kwargs: dict):
    '''Fills in the config dict with the settings based on its name'''

    for key, value in kwargs.items():
        key_list = key.replace("[]", "").split("_")
        add_val_to_config(CONFIG, key_list, value)


def add_val_to_config(config: ConfigList, key_list: list, value):
    '''recursive way of adding value into the config'''
    if len(key_list) == 1:
        if key_list[0] in config.keys():
            config[key_list[0]].value = value
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
            return add_val_to_config(config[key_list[0]], key_list[1:], value)

        for obj in config:
            if obj.is_section:
                return add_val_to_config(obj, key_list, value)
