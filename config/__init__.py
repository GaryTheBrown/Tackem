"""The CONFIG Options for the system"""
from config.api import api_config
from config.backend.list import ConfigList
from config.database import database_config
from config.libraries import libraries_config
from config.musicbrainz import musicbrainz_config
from config.ripper import ripper_config
from config.scraper import scraper_config
from config.webui import webui_config

CONFIG = ConfigList("root", "Root")
CONFIG.append(database_config())
CONFIG.append(webui_config())
CONFIG.append(api_config())
CONFIG.append(libraries_config())
CONFIG.append(ripper_config())
CONFIG.append(scraper_config())
CONFIG.append(musicbrainz_config())
