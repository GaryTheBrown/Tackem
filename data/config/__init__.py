"""The CONFIG Options for the system"""
from data.config.api import api_config
from data.config.database import database_config
from data.config.libraries import libraries_config
from data.config.musicbrainz import musicbrainz_config
from data.config.ripper import ripper_config
from data.config.scraper import scraper_config
from data.config.webui import webui_config
from libs.config.list import ConfigList

CONFIG = ConfigList("root", "Root")
CONFIG.append(database_config())
CONFIG.append(webui_config())
CONFIG.append(api_config())
CONFIG.append(libraries_config())
CONFIG.append(ripper_config())
CONFIG.append(scraper_config())
CONFIG.append(musicbrainz_config())
