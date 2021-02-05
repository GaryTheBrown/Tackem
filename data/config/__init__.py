'''The Config Options for the system'''
from libs.config.list import ConfigList
from .api import api_config
from .database import database_config
from .libraries import libraries_config
from .musicbrainz import musicbrainz_config
from .ripper import ripper_config
from .scraper import scraper_config
from .webui import webui_config

CONFIG = ConfigList("root", "Root")
CONFIG.append(database_config())
CONFIG.append(webui_config())
CONFIG.append(api_config())
CONFIG.append(libraries_config())
CONFIG.append(ripper_config())
CONFIG.append(ConfigList("plugins", "Plugins"))
CONFIG.append(scraper_config())
CONFIG.append(musicbrainz_config())
