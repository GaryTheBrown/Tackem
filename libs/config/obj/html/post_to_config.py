'''Config File Setup'''
from config_data import CONFIG
from libs.config.list import ConfigList

def post_config_settings(kwargs: dict, config) -> None:
    '''Fills in the config dict with the settings based on its name'''

    for key, value in kwargs.items():
        key_list = key.replace("[]", "").split("_")
        add_val_to_config(CONFIG, config, key_list, value)


def add_val_to_config(config_obj: ConfigList, config, key_list: list, value) -> None:
    '''recursive way of adding value into the config'''
    if len(key_list) == 1:
        config[key_list[0]] = config_obj[key_list[0]].to_type(value)
    else:
        if not config or key_list[0] not in config:
            config[key_list[0]] = {}
        add_val_to_config(config_obj[key_list[0]], config[key_list[0]], key_list[1:], value)


#TODO MEED TO TAKE INTO ACCOUNT THE SINGLE INSTANCE SOMEWHERE HERE.
