'''Config File Setup'''
from configobj import ConfigObj
from validate import Validator
from libs.config.configobj_extras import EXTRA_FUNCTIONS
from libs.config.data import CONFIG


def config_load(path: str):
    """Create a config file using a configspec and validate it against a Validator object"""
    temp_spec = CONFIG.get_root_spec
    spec = temp_spec.split("\n")
    config = ConfigObj(path + "config.ini", configspec=spec)
    validator = Validator(EXTRA_FUNCTIONS)
    config.validate(validator, copy=True)
    config.filename = path + "config.ini"
    # line bellow for debugging
    # print(config)
    return config
