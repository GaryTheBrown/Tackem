"""CONFIG List Class"""
from libs.config.list.file import ConfigListFile
from libs.config.list.html import ConfigListHtml


class ConfigList(ConfigListHtml, ConfigListFile):
    """Main Point of access for config list"""
