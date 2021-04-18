"""Libraries Config"""
from config.backend.list import ConfigList
from config.backend.obj.boolean import ConfigObjBoolean
from config.backend.obj.data.option import ConfigObjOption
from config.backend.obj.enabled import ConfigObjEnabled
from config.backend.obj.options.select import ConfigObjOptionsSelect
from config.backend.obj.string import ConfigObjString
from config.backend.obj.string_list import ConfigObjStringList


def libraries_config() -> ConfigList:
    """Libraries Config"""
    return ConfigList(
        "libraries",
        "Libraries",
        ConfigList(
            "global",
            "Global",
            ConfigList(
                "autofilecheck",
                "Auto File Check",
                ConfigObjOptionsSelect(
                    "regularity",
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
                    "Auto File Check ",
                    "How often to automatically check the files for corruption",
                ),
                ConfigObjBoolean("log", True, "Log", "should I log all runs of the filechecker?"),
            ),
            ConfigList(
                "extensions",
                "Extensions",
                ConfigObjStringList(
                    "video",
                    ["mkv", "avi", "mp4", "m2ts"],
                    "Video File Extensions",
                    "what extensions are linked to video files",
                ),
                ConfigObjStringList(
                    "audio",
                    ["mp3", "ogg", "flac"],
                    "Audio File Extensions",
                    "what extensions are linked to audio files",
                )
                # Game Extensions will go into a folder that stores info on each system supported
            ),
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
                    "Where is the library stored?",
                ),
            ),
            # This should be generated from the folder that stores info on each system supported.
            many_section_limit_list=["SNES", "NES"],
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
                    "Where is the library stored?",
                ),
            ),
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
                    "Where is the library stored?",
                ),
            ),
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
                    "Where is the library stored?",
                ),
            ),
        ),
    )
