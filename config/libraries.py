"""Libraries Config"""
from config.backend.list import ConfigList
from config.backend.obj.boolean import ConfigObjBoolean
from config.backend.obj.data.checkbox import ConfigObjCheckbox
from config.backend.obj.data.option import ConfigObjOption
from config.backend.obj.options.checkbox import ConfigObjOptionsCheckBox
from config.backend.obj.options.select import ConfigObjOptionsSelect
from config.backend.obj.string import ConfigObjString
from config.backend.obj.string_list import ConfigObjStringList
from data.qualities import Qualities


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
            "movies",
            "Movie Options",
            ConfigObjStringList(
                "extensions",
                ["mkv", "avi", "mp4", "m2ts"],
                "Video File Extensions",
                "what extensions are linked to video files",
            ),
            ConfigObjString(
                "location",
                "Library/Movies/",
                "Location",
                "Where is the library stored?",
            ),
            ConfigObjOptionsCheckBox(
                "allowed",
                Qualities.config_option(ConfigObjCheckbox),
                Qualities.config_values(),
                "Allowed Qualities",
                "What Qualities are allowed in the Library",
            ),
            ConfigObjOptionsCheckBox(
                "last",
                Qualities.config_option(ConfigObjCheckbox),
                [],
                "Saved Qualities",
                "What Quality/Qualities are saved in the Library",
            ),
        ),
        ConfigList(
            "tvshows",
            "TV Show Options",
            ConfigObjStringList(
                "extensions",
                ["mkv", "avi", "mp4", "m2ts"],
                "Video File Extensions",
                "what extensions are linked to video files",
            ),
            ConfigObjString(
                "location",
                "Library/TVShows/",
                "Location",
                "Where is the library stored?",
            ),
            ConfigObjOptionsCheckBox(
                "allowed",
                Qualities.config_option(ConfigObjCheckbox),
                Qualities.config_values(),
                "Allowed Qualities",
                "What Qualities are allowed in the Library",
            ),
            ConfigObjOptionsCheckBox(
                "last",
                Qualities.config_option(ConfigObjCheckbox),
                [],
                "Saved Qualities",
                "What Quality/Qualities are saved in the Library",
            ),
        ),
        ConfigList(
            "music",
            "Music Options",
            ConfigObjStringList(
                "extensions",
                ["mp3", "ogg", "flac"],
                "Audio File Extensions",
                "what extensions are linked to audio files",
            ),
            ConfigObjString(
                "location",
                "Library/Music/",
                "Location",
                "Where is the library stored?",
            ),
        ),
    )
