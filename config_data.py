'''The Config Options for the system'''
import os
from libs.config.list import ConfigList
from libs.config.obj.string import ConfigObjString
from libs.config.obj.password import ConfigObjPassword
from libs.config.obj.integer_number import ConfigObjIntegerNumber
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.button import Button
from libs.config.obj.enabled import ConfigObjEnabled
from libs.config.obj.boolean import ConfigObjBoolean
from libs.config.obj.options.radio import ConfigObjOptionsRadio
from libs.config.obj.data.radio import ConfigObjRadio
from libs.config.obj.options.select import ConfigObjOptionsSelect
from libs.config.obj.data.option import ConfigObjOption
from libs.data.locale_options import OPTIONS as locale_options
from libs.startup_arguments import THEMEFOLDERLOCATION

CONFIG = ConfigList(
    "root",
    "Root",
    # ConfigList(
    #     "authentication",
    #     "Authentication"
    # ),
    ConfigList(
        "database",
        "Database",
        ConfigObjOptionsRadio(
            "mode",
            [
                ConfigObjRadio(
                    "sqlite3",
                    "SQLite3",
                    input_attributes=InputAttributes(
                        data_hide="database_mysql_section"
                    )
                ),
                ConfigObjRadio(
                    "mysql",
                    "MYSQL",
                    input_attributes=InputAttributes(
                        disabled=True,
                        data_show="database_mysql_section"
                    )
                )
            ],
            "sqlite3",
            "Database Mode",
            "What system do you want to use for data?"
        ),
        ConfigList(
            "mysql",
            "MYSQL",
            ConfigObjString(
                "address",
                "localhost",
                "Database Address",
                "The Database Address Name or IP"
            ),
            ConfigObjIntegerNumber(
                "port",
                3306,
                "Database Port",
                "The port your database is open on",
                input_attributes=InputAttributes(
                    min=1001,
                    max=65535
                )
            ),
            ConfigObjString(
                "username",
                "",
                "Database Username",
                "The username for access to the database"
            ),
            ConfigObjPassword(
                "password",
                "Database Password",
                "The password for access to the database"
            ),
            ConfigObjString(
                "name",
                "tackem",
                "Database Name",
                "The name of the database"
            ),
            is_section=True
        )
    ),
    ConfigList(
        "api",
        "API Interface",
        ConfigObjString(
            "masterkey",
            "",
            "Master API Key",
            "The master API key for full control",
            button=Button(
                "Generate API Key",
                "generateAPIKey",
                True,
                input="api_masterkey"
            ),
            input_attributes=InputAttributes("readonly")
        ),
        ConfigObjString(
            "userkey",
            "",
            "User API Key",
            "The user API key for limited control",
            button=Button(
                "Generate API Key",
                "generateAPIKey",
                True,
                input="api_userkey"
            ),
            input_attributes=InputAttributes("readonly")
        )
    ),
    ConfigList(
        "libraries",
        "Libraries",
        ConfigList(
            "global",
            "Global",
            ConfigObjOptionsSelect(
                "autofilecheck",
                [
                    ConfigObjOption("disabled", "Disabled"),
                    ConfigObjOption("hourly", "Hourly"),
                    ConfigObjOption("daily", "Daily"),
                    ConfigObjOption("weekly", "Weekly"),
                    ConfigObjOption("monthly", "Monthly"),
                    ConfigObjOption("quaterly", "Quaterly"),
                    ConfigObjOption("halfyear", "Half Yearly"),
                    ConfigObjOption("year", "Yearly"),
                ],
                "monthly",
                "Auto File Check",
                "How often to automatically check the files for corruption"
            )
        ),
        ConfigList(
            "games",
            "Games",
            many_section=ConfigList(
                "",
                "",
                ConfigObjEnabled(),
                ConfigObjString(
                    "location",
                    "Library/Games/",
                    "Games Library Location",
                    "Where is the library stored?"
                )
            ),
            many_section_limit_list=[
                "SNES", "NES"
            ]
        ),
        ConfigList(
            "movies",
            "Movies",
            many_section=ConfigList(
                "",
                "",
                ConfigObjEnabled(),
                ConfigObjString(
                    "location",
                    "Library/Movies/",
                    "Movies Location",
                    "Where is the library stored?"
                )
            )
        ),
        ConfigList(
            "tvshows",
            "TV Shows",
            many_section=ConfigList(
                "",
                "",
                ConfigObjEnabled(),
                ConfigObjString(
                    "location",
                    "Library/TVShows/",
                    "TV Show Location",
                    "Where is the library stored?"
                )
            )
        ),
        ConfigList(
            "music",
            "Music",
            many_section=ConfigList(
                "",
                "",
                ConfigObjEnabled(),
                ConfigObjString(
                    "location",
                    "Library/Music/",
                    "Music Location",
                    "Where is the library stored?"
                )
            )
        )
    ),
    ConfigList(
        "plugins",
        "Plugins"
    ),
    ConfigList(
        "webui",
        "Web Interface",
        ConfigObjIntegerNumber(
            "port",
            8081,
            "Port",
            "The port the system is accessed on",
            input_attributes=InputAttributes(
                min=1001,
                max=65535
            )
        ),
        ConfigObjString(
            "baseurl",
            "/",
            "Base Url",
            "The Base Url must start and end with '/'"
        ),
        ConfigObjOptionsSelect(
            "theme",
            [ConfigObjOption(x, x) for x in next(os.walk(THEMEFOLDERLOCATION))[1]],
            "default",
            "Theme",
            "The Theme for the system"
        )
    ),
    ConfigList(
        "scraper",
        "Video Scraper (The Movie DB)",
        ConfigObjString(
            "apikey",
            "",
            "API Key",
            "The API key for TMDB API access goto http://www.themoviedb.org/ to grab your key",
        ),
        ConfigObjString(
            "url",
            "api.themoviedb.org",
            "Base Url",
            "The API base url for TMDB API access Leave alone unless you need to move this"
        ),
        ConfigObjBoolean(
            "includeadult",
            False,
            "",
            "",
            hide_on_html=True
        ),
        ConfigObjOptionsSelect(
            "language",
            locale_options,
            "en-gb",
            "Language",
            "language to use when scraping the data"
        )
    ),
    ConfigList(
        "musicbrainz",
        "Audio CD Scraper (MusicBrainz)",
        ConfigObjString(
            "username",
            "",
            "MusicBrainz Username",
            """
Your MusicBrainz username (Only needed if you are submitting unknown CDs Back to the service)"""
        ),
        ConfigObjPassword(
            "password",
            "MusicBrainz Password",
            """
Your MusicBrainz password (Only needed if you are submitting unknown CDs Back to the service)"""
        ),
        ConfigObjString(
            "url",
            "musicbrainz.org",
            "Base Url",
            """
The base url for MusicBrainz access Leave alone unless you need to move this"""
        ),
        ConfigObjString(
            "coverarturl",
            "coverartarchive.org",
            "Cover Art Base Url",
            "The base url for Cover Art Archive requests Leave alone unless you need to move this"
        )
    )
)
