"""CONFIG List Class"""
from config.backend.list.file import ConfigListFile
from config.backend.list.html import ConfigListHtml


class ConfigList(ConfigListHtml, ConfigListFile):
    """Main Point of access for config list"""
