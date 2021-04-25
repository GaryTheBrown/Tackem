"""Libraries Config"""
from config.backend.list import ConfigList
from config.backend.obj.boolean import ConfigObjBoolean
from config.backend.obj.data.option import ConfigObjOption
from config.backend.obj.options.select import ConfigObjOptionsSelect
from config.backend.obj.string import ConfigObjString
from config.backend.obj.string_list import ConfigObjStringList


def libraries_config() -> ConfigList:
    """Libraries Config"""
    return ConfigList(
        "libraries",
        "Libraries",
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
            ),
        ),
        ConfigList(
            "locations",
            "Base Locations",
            ConfigObjString(
                "movies",
                "Library/Movies/",
                "Movies Location",
                "Where is the library stored?",
            ),
            ConfigObjString(
                "tvshows",
                "Library/TVShows/",
                "TV Show Location",
                "Where is the library stored?",
            ),
            ConfigObjString(
                "music",
                "Library/Music/",
                "Music Location",
                "Where is the library stored?",
            ),
        ),
    )
