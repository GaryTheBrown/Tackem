'''The Config Options for the system'''
from libs.config.list import ConfigList
from libs.config.obj.string import ConfigObjString
from libs.config.obj.integer_number import ConfigObjIntegerNumber
from libs.config.obj.password import ConfigObjPassword
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.button import Button
from libs.config.obj.boolean import ConfigObjBoolean
from libs.config.obj.options_radio import ConfigObjOptionsRadio
from libs.config.obj.data.radio import ConfigObjRadio

CONFIG = ConfigList(
    "root",
    "Root",
    ConfigObjBoolean(
        "firstrun",
        True,
        "First Run",
        "",
        True
    ),
    ConfigList(
        "authentication",
        "Authentication",

    ),
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
                        data_hide="database_mysql"
                    )
                ),
                ConfigObjRadio(
                    "mysql",
                    "MYSQL",
                    input_attributes=InputAttributes(
                        disabled=True,
                        data_show="database_mysql"
                    )
                )
            ],
            0,
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
                "",
                "Database Password",
                "The password for access to the database"
            ),
            ConfigObjString(
                "name",
                "tackem",
                "Database Name",
                "The name of the database"
            )
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
            button=Button("Generate API Key", "generateAPIKey", True, input="api_masterkey")
        ),
        ConfigObjString(
            "userkey",
            "",
            "User API Key",
            "The user API key for limited control",
            button=Button("Generate API Key", "generateAPIKey", True, input="api_userkey")
        )
    ),


    ConfigList("plugins", "Plugins")
)

# CONFIG.append(
#     ConfigList("webui", "Web Interface", objects=[
#         ConfigObject("disabled", "Disabled", "boolean", default=False, toggle_section="webui",
#                      input_type="switch", hide_from_html=True),
#         ConfigObject("port", "Port", "integer", minimum=1001, maximum=65535, default=8081,
#                      help_text="The port for the WebUI"),
#         ConfigObject("baseurl", "Base Url", "string", default="/", help_text="""The Base URL
# must start with '/'""")
#     ])
# )
# CONFIG.append(
#     ConfigList("scraper", "Video Scraper (The Movie DB)", objects=[
#         ConfigObject("enabled", "Enabled", "boolean", default=False, toggle_section="scraper",
#                      input_type="switch"),
#         ConfigObject("apikey", "API Key", "string", default='', help_text="""
# The API key for TMDB API access goto http://www.themoviedb.org/ to grab your key"""),
#         ConfigObject("url", "Base Url", "string", default='api.themoviedb.org', help_text="""
# The API base url for TMDB API access Leave alone unless you need to move this"""),
#         ConfigObject("includeadult", "", "boolean", default=False, hide_from_html=True),
#         ConfigObject("language", "Language", "option", input_type="dropdown", default='en-GB',
#                      options=locale_options, help_text="language to use when scraping the data"),
#     ])
# )
# CONFIG.append(
#     ConfigList("musicbrainz", "Audio CD Scraper (MusicBrainz)", objects=[
#         ConfigObject("enabled", "Enabled", "boolean", default=False, toggle_section="musicbrainz",
#                      input_type="switch"),
#         ConfigObject("username", "MusicBrainz Username", "string", default="", help_text="""
# Your MusicBrainz username (Only needed if you are submitting unknown CDs Back to the service)"""),
#         ConfigObject("password", "MusicBrainz Password", "password", default="", help_text="""
# Your MusicBrainz password (Only needed if you are submitting unknown CDs Back to the service)"""),
#         ConfigObject("url", "Base Url", "string", default='musicbrainz.org', help_text="""
# The base url for MusicBrainz access Leave alone unless you need to move this"""),
#         ConfigObject("coverarturl", "Cover Art Base Url", "string", default='coverartarchive.org',
#                      help_text="""
# The base url for Cover Art Archive requests Leave alone unless you need to move this""")
#     ])
# )
