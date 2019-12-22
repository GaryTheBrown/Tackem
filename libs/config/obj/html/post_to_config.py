'''Config File Setup'''

def post_config_settings(kwargs: dict, config) -> None:
    '''Fills in the config dict with the settings based on its name'''



    for key in kwargs:
        key_list = key.replace("[]", "").split("_")
        if key_list[0] == "cs":
            value = None
            if key_list[1] == "plugins":
                if key_list[2] in plugins and key_list[3] in plugins[key_list[2]]:
                    plugin = plugins[key_list[2]][key_list[3]]
                    if plugin.SETTINGS['single_instance']:
                        value = plugin.CONFIG.convert_var(key_list[4:], kwargs[key])
                    else:
                        value = plugin.CONFIG.convert_var(key_list[5:], kwargs[key])
            else:
                value = CONFIG.convert_var(key_list[1:], kwargs[key])

            if value is not None:
                add_val_to_config(config, key_list[1:], value)


def add_val_to_config(config, key_list: list, value) -> None:
    '''recursive way of adding value into the config'''
    if len(key_list) == 1:
        config[key_list[0]] = value
    else:
        if not config:
            config[key_list[0]] = {}
        elif key_list[0] not in config:
            config[key_list[0]] = {}
        add_val_to_config(config[key_list[0]], key_list[1:], value)
