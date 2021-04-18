"""Musicbrainz Config"""
from config.backend.list import ConfigList
from config.backend.obj.password import ConfigObjPassword
from config.backend.obj.string import ConfigObjString


def musicbrainz_config() -> ConfigList:
    """Musicbrainz Config"""
    ConfigList(
        "musicbrainz",
        "Audio CD Scraper (MusicBrainz)",
        ConfigObjString(
            "username",
            "",
            "MusicBrainz Username",
            """
Your MusicBrainz username (Only needed if you are submitting unknown CDs Back to the service)""",
        ),
        ConfigObjPassword(
            "password",
            "MusicBrainz Password",
            """
Your MusicBrainz password (Only needed if you are submitting unknown CDs Back to the service)""",
        ),
        ConfigObjString(
            "url",
            "musicbrainz.org",
            "Base Url",
            "The base url for MusicBrainz access Leave alone unless you need to move this",
        ),
        ConfigObjString(
            "coverarturl",
            "coverartarchive.org",
            "Cover Art Base Url",
            "The base url for Cover Art Archive requests Leave alone unless you need to move this",
        ),
    )
