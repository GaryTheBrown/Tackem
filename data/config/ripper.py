'''Ripper Config'''
import platform
from data.audio_format_options import audio_format_options
from data.languages import Languages
from libs.config.list import ConfigList
from libs.config.rules import ConfigRules
from libs.config.obj.boolean import ConfigObjBoolean
from libs.config.obj.enabled import ConfigObjEnabled
from libs.config.obj.integer_number import ConfigObjIntegerNumber
from libs.config.obj.string import ConfigObjString
from libs.config.obj.data.checkbox import ConfigObjCheckbox
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.option import ConfigObjOption
from libs.config.obj.data.radio import ConfigObjRadio
from libs.config.obj.options.radio import ConfigObjOptionsRadio
from libs.config.obj.options.select import ConfigObjOptionsSelect
from libs.config.obj.options.checkbox import ConfigObjOptionsCheckBox
from libs.hardware import Hardware
from libs.program_checker import check_for_required_programs
from presets import video_presets_config_options

RIPPERREQUIREDLINUX = [
    "hwinfo",
    "makemkvcon",
    "java",
    "ccextractor",
    "ffmpeg",
    "ffprobe",
    "mplayer",
    "eject",
    "lsblk",
    "hwinfo",
    "blkid"
]

def ripper_config() -> ConfigList:
    '''Ripper Config'''
    if platform.system() != 'Linux':
        return None
    if not check_for_required_programs(RIPPERREQUIREDLINUX, "Ripper"):
        return None


    config = ConfigList(
        "ripper",
        "Ripper",
        ConfigObjEnabled(),
        ConfigList(
            "locations",
            "Folder Location",
            ConfigObjString(
                "videoripping",
                "videoripping/",
                "Video Ripping Location",
                "Where do you want to store video discs while ripping them?"
            ),
            ConfigObjString(
                "videoripped",
                "videoripped/",
                "Video Ripped Location",
                "Where do you want to move the video discs to when completed"
            ),
            ConfigObjString(
                "audioripping",
                "audioripping/",
                "Audio Ripping Location",
                "Where do you want to store audio cds while ripping them?"
            ),
            ConfigObjString(
                "audioripped",
                "audioripped/",
                "Audio Ripped Location",
                "Where do you want to move the audio cds to when completed"
            )
        ),
        ConfigList(
            "videoripping",
            "Video Ripping",
            ConfigObjEnabled(),
            ConfigObjOptionsCheckBox(
                "torip",
                [
                    ConfigObjCheckbox("movie", "Movie"),
                    ConfigObjCheckbox("tvshow", "TV Show Episode"),
                    ConfigObjCheckbox("trailer", "Trailer"),
                    ConfigObjCheckbox("extra", "Extra"),
                    ConfigObjCheckbox("other", "Other")
                ],
                ["movie", "tvshow", "other"],
                "What to Rip",
                "What File Types do you want to rip and include"
            )
        ),
        ConfigList(
            "audioripping",
            "Audo CD Ripping",
            ConfigObjEnabled(),
        ),
        ConfigList(
            "converter",
            "Converter",
            ConfigObjEnabled(),
            ConfigObjString(
                "ffmpeglocation",
                "ffmpeg",
                "FFmpeg Location",
                "Where is FFmpeg located?"
            ),
            ConfigObjString(
                "ffprobelocation",
                "ffprobe",
                "FFprobe Location",
                "Where is FFprobe located?"
            ),
            ConfigObjIntegerNumber(
                "threadcount",
                1,
                "How Many Instances?",
                "How Many Threads (Max of 5)",
                input_attributes=InputAttributes(
                    min=1,
                    max=5
                )
            ),
            ConfigObjBoolean(
                "keeporiginalfile",
                False,
                "Keep Original File",
                "If you want to keep the original file after backup"
            ),
            ConfigObjOptionsSelect(
                "defaultlanguage",
                Languages().config_option_3t(ConfigObjOption),
                "eng",
                "Default Language",
                "What is your main language?"
            ),
            ConfigObjBoolean(
                "videoinserttags",
                True,
                "Insert Tags",
                "Do you want to add in the tags to the Video Files?"
            ),
            ConfigObjOptionsSelect(
                "video3dtype",
                [
                    ConfigObjOption("keep", "Keep Original"),
                    ConfigObjOption("sbsl", "Side by Side (Left Eye First)"),
                    ConfigObjOption("sbsr", "Side by Side (Right Eye First)"),
                    ConfigObjOption("sbs2l", "Half Side by Side (Left Eye First)"),
                    ConfigObjOption(
                        "sbs2r", "Half Side by Side (Right Eye First)"),
                    ConfigObjOption("abl", "Top Bottom (Left Eye Top)"),
                    ConfigObjOption("abr", "Top Bottom (Right Eye Top)"),
                    ConfigObjOption("ab2l", "Half Top Bottom (Left Eye Top)"),
                    ConfigObjOption("ab2r", "Half Top Bottom (Right Eye Top)"),
                    ConfigObjOption("al", "Alternating Frames (Left Eye First)"),
                    ConfigObjOption("ar", "Alternating Frames (Right Eye First)"),
                    ConfigObjOption(
                        "irl", "Interleaved Rows (Left Eye Has Top Row)"),
                    ConfigObjOption(
                        "irr", "Interleaved Rows (Right Eye Has Top Row)"),
                    ConfigObjOption("arbg", "Anaglyph Red/Blue Grayscale"),
                    ConfigObjOption("argg", "Anaglyph Red/Green Grayscale"),
                    ConfigObjOption("arcg", "Anaglyph Red/Cyan Grayscale"),
                    ConfigObjOption("arch", "Anaglyph Red/Cyan Half Coloured"),
                    ConfigObjOption("arcc", "Anaglyph Red/Cyan Colour"),
                    ConfigObjOption("arcd", "Anaglyph Red/Cyan Colour dubois"),
                    ConfigObjOption("agmg", "Anaglyph Green/Magenta Grayscale"),
                    ConfigObjOption(
                        "agmh", "Anaglyph Green/Magenta Half Coloured"),
                    ConfigObjOption("agmc", "Anaglyph Green/Magenta Coloured"),
                    ConfigObjOption(
                        "agmd", "Anaglyph Green/Magenta Colour Dubois"),
                    ConfigObjOption("aybg", "Anaglyph Yellow/Blue Grayscale"),
                    ConfigObjOption("aybh", "Anaglyph Yellow/Blue Half Coloured"),
                    ConfigObjOption("aybc", "Anaglyph Yellow/Blue Coloured"),
                    ConfigObjOption("aybd", "Anaglyph Yellow/Blue Colour Dubois"),
                    ConfigObjOption("ml", "Mono Output (Left Eye Only)"),
                    ConfigObjOption("mr", "Mono Output (Right Eye Only)"),
                    ConfigObjOption("chl", "Checkerboard (Left Eye First)"),
                    ConfigObjOption("chr", "Checkerboard (Right Eye First)"),
                    ConfigObjOption("icl", "Interleaved Columns (Left Eye First)"),
                    ConfigObjOption(
                        "icr", "Interleaved Columns (Right Eye First)"),
                    ConfigObjOption("hdmi", "HDMI Frame Pack")
                ],
                'keep',
                "3D Type",
                "what 3D mode do you want to transform 3d Discs into"
            ),
            ConfigObjOptionsSelect(
                "videoresolution",
                [
                    ConfigObjOption("keep", "Keep Original"),
                    ConfigObjOption("2160", "4K"),
                    ConfigObjOption("1080", "1080"),
                    ConfigObjOption("720", "720"),
                    ConfigObjOption("sd", "SD")
                ],
                'keep',
                "Max Video Resolution",
                "What is the maximum resolution you want to keep or downscale to?"
            ),
            ConfigObjOptionsRadio(
                "videocodec",
                [
                    ConfigObjRadio(
                        "keep",
                        "Keep Original",
                        input_attributes=InputAttributes(
                            data_hide=[
                                "ripper_converter_videopresets",
                                "ripper_converter_x26custom"
                            ]
                        )
                    ),
                    ConfigObjRadio(
                        "x264default",
                        "X264 Default",
                        input_attributes=InputAttributes(
                            data_hide=[
                                "ripper_converter_videopresets",
                                "ripper_converter_x26custom"
                            ]
                        )
                    ),
                    ConfigObjRadio(
                        "x265default",
                        "X265 Default",
                        input_attributes=InputAttributes(
                            data_hide=[
                                "ripper_converter_videopresets",
                                "ripper_converter_x26custom"
                            ]
                        )
                    ),
                    ConfigObjRadio(
                        "x264custom",
                        "X264 Custom",
                        input_attributes=InputAttributes(
                            data_show="ripper_converter_x26custom",
                            data_hide="ripper_converter_videopresets"
                        )
                    ),
                    ConfigObjRadio(
                        "x265custom",
                        "X265 Custom",
                        input_attributes=InputAttributes(
                            data_show="ripper_converter_x26custom",
                            data_hide="ripper_converter_videopresets"
                        )
                    ),
                    ConfigObjRadio(
                        "preset",
                        "Preset (choose from a list)",
                        input_attributes=InputAttributes(
                            data_show="ripper_converter_videopresets",
                            data_hide="ripper_converter_x26custom"
                        )
                    )
                ],
                'keep',
                "Video Codec",
                "What video codec do you wish to convert to?"
            ),
            ConfigList(
                "videopresets",
                "Video Preset List",
                ConfigObjOptionsSelect(
                    "videopreset",
                    video_presets_config_options(ConfigObjOption),
                    "",
                    "Video Preset",
                    "What preset do you want to use?"
                ),
                is_section=True
            ),
            ConfigList(
                "x26custom",
                "x26? Custom Options",
                ConfigObjIntegerNumber(
                    "x26crf8bit",
                    23,
                    "CRF (8 bit)?",
                    """
The range of the CRF (8 bit) scale is 0–51, where 0 is lossless, 23 is the default,and 51 is worst
quality possible. A lower value generally leads to higher quality, and a subjectively sane range is
17–28. Consider 17 or 18 to be visually lossless or nearly so; it should look the same or nearly the
same as the input but it isn't technically lossless. The range is exponential, so increasing the CRF
value +6 results in roughly half the bitrate / file size, while -6 leads to roughly twice the
bitrate. Choose the highest CRF value that still provides an acceptable quality. If the output looks
good, then try a higher value. If it looks bad, choose a lower value.""",
                    input_attributes=InputAttributes(
                        min=0,
                        max=51
                    )
                ),
                ConfigObjIntegerNumber(
                    "x26crf10bit",
                    23,
                    "CRF (10 bit)?",
                    """
The range of the CRF (10 bit) scale is 0–63, where 0 is lossless, 23 is the default,and 63 is worst
quality possible.""",
                    input_attributes=InputAttributes(
                        min=0,
                        max=63,
                    )
                ),
                ConfigObjOptionsSelect(
                    "x26preset",
                    [
                        ConfigObjOption("ultrafast", "Ultra Fast"),
                        ConfigObjOption("superfast", "Super Fast"),
                        ConfigObjOption("veryfast", "Very Fast"),
                        ConfigObjOption("faster", "Faster"),
                        ConfigObjOption("fast", "Fast"),
                        ConfigObjOption("medium", "Medium"),
                        ConfigObjOption("slow", "Slow"),
                        ConfigObjOption("slower", "Slower"),
                        ConfigObjOption("veryslow", "Very Slow")
                    ],
                    "medium",
                    "Preset",
                    """
A preset is a collection of options that will provide a certain encoding speed to compression ratio.
A slower preset will provide better compression (compression is quality per filesize).
This means that, for example, if you target a certain file size or constant bit rate,
you will achieve better quality with a slower preset. Similarly, for constant quality encoding,
you will simply save bitrate by choosing a slower preset.
Use the slowest preset that you have patience for."""
                ),
                ConfigObjString(
                    "x26extra",
                    "",
                    "Extra commands",
                    "Other commands?"
                ),
                is_section=True
            ),
            ConfigObjOptionsRadio(
                "originalordub",
                [
                    ConfigObjRadio("original", "Original"),
                    ConfigObjRadio("dub", "Dubbed")
                ],
                'all',
                "Original or Dubbed Language",
                """
Do you want the default stream to be the Original language or dubbed in your language if available?
"""
            ),
            ConfigObjOptionsRadio(
                "audiolanguage",
                [
                    ConfigObjRadio(
                        "all",
                        "All",
                        input_attributes=InputAttributes(
                            data_hide="ripper_converter_audiolanglist"
                        )
                    ),
                    ConfigObjRadio(
                        "original",
                        "Original Language Only",
                        input_attributes=InputAttributes(
                            data_hide="ripper_converter_audiolanglist"
                        )
                    ),
                    ConfigObjRadio(
                        "selectedandoriginal",
                        "Original Language + Selected Languages",
                        input_attributes=InputAttributes(
                            data_show="ripper_converter_audiolanglist"
                        )
                    ),
                    ConfigObjRadio(
                        "selected",
                        "Selected Languages",
                        input_attributes=InputAttributes(
                            data_show="ripper_converter_audiolanglist"
                        )
                    )
                ],
                'all',
                "Audio Languages",
                "What Audio Languages do you want to keep?"
            ),
            ConfigList(
                "audiolanglist",
                "Audio Language List",
                ConfigObjOptionsCheckBox(
                    "audiolanguages",
                    Languages().config_option_3t(ConfigObjCheckbox),
                    "eng",
                    "Audio Languages",
                    "",
                ),
                is_section=True,
            ),
            ConfigObjOptionsSelect(
                "audioformat",
                [
                    ConfigObjOption(
                        "all",
                        "All",
                        input_attributes=InputAttributes(
                            data_hide="ripper_converter_audioformatlist"
                        )
                    ),
                    ConfigObjOption(
                        "highest",
                        "Highest Quality",
                        input_attributes=InputAttributes(
                            disabled=True,
                            data_hide="ripper_converter_audioformatlist"
                        )
                    ),
                    ConfigObjOption(
                        "selected",
                        "Selected Formats",
                        input_attributes=InputAttributes(
                            data_show="ripper_converter_audioformatlist"
                        )
                    ),
                    ConfigObjOption(
                        "convert",
                        "Convert to Selected Formats",
                        input_attributes=InputAttributes(
                            disabled=True,
                            data_show="ripper_converter_audioformatlist"
                        )
                    )
                ],
                'all',
                "Audio Format",
                "What Audio Formats do you want to keep?"
            ),
            ConfigList(
                "audioformatlist",
                "Audio Format List",
                ConfigObjOptionsCheckBox(
                    "audioformats",
                    audio_format_options(ConfigObjCheckbox),
                    "",
                    "Audio Formats",
                    ""
                ),
                is_section=True
            ),
            ConfigObjBoolean(
                "keepcommentary",
                True,
                "Keep Commentary",
                "Do you want to keep the commentary track(s)?"
            ),
            ConfigObjBoolean(
                "keepchapters",
                True,
                "Keep Chapters",
                "Do you want to keep the chapter points?"
            ),
            ConfigObjOptionsSelect(
                "subtitle",
                [
                    ConfigObjOption(
                        "all",
                        "All",
                        input_attributes=InputAttributes(
                            data_hide="ripper_converter_subtitleslist"
                        )
                    ),
                    ConfigObjOption(
                        "none",
                        "None",
                        input_attributes=InputAttributes(
                            data_hide="ripper_converter_subtitleslist"
                        )
                    ),
                    ConfigObjOption(
                        "selected",
                        "Selected Subtitles",
                        input_attributes=InputAttributes(
                            data_show="ripper_converter_subtitleslist"
                        )
                    )
                ],
                'all',
                "Subtitles",
                "What subtitles do you want to keep?"
            ),
            ConfigList(
                "subtitleslist",
                "Subtitle List",
                ConfigObjOptionsCheckBox(
                    "subtitlelanguages",
                    Languages().config_option_3t(ConfigObjCheckbox),
                    "",
                    "Subtitle Languages",
                    ""
                ),
                is_section=True
            ),
            ConfigObjBoolean(
                "keepclosedcaptions",
                True,
                "Keep Closed Captions",
                "Do you want to keep the closed captions?"
            ),
        )
    )

    if Hardware.disc_drives():
        config.append(
            ConfigObjOptionsRadio(
                "mode",
                [
                    ConfigObjRadio(
                        "drive",
                        "Drive",
                        input_attributes=InputAttributes(
                            data_hide=[
                                "ripper_locations_videoiso",
                                "ripper_locations_audioiso"
                            ],
                            data_show="ripper_drives"
                        )
                    ),
                    ConfigObjRadio(
                        "iso",
                        "ISO",
                        input_attributes=InputAttributes(
                            data_show=[
                                "ripper_locations_videoiso",
                                "ripper_locations_audioiso"
                            ],
                            data_hide="ripper_drives"
                        )
                    )
                ],
                "drive" if Hardware.disc_drives() else "iso",
                "Ripping Mode",
                "Rip from Drives or from ISO files"
            )
        )

    config.append(
        ConfigList(
            "isolocations",
            "Folder Location",
            ConfigObjString(
                "videoiso",
                "videoiso/",
                "Video ISO Location",
                "Where do you want to watch for video ISOs?"
            ),
            ConfigObjString(
                "audioiso",
                "audioiso/",
                "Audio ISO Location",
                "Where do you want to watch for audio ISOs?"
            )
        )
    )

    if Hardware.disc_drives():
        config.append(
            ConfigList(
                "drives",
                "Drives",
                many_section=ConfigList(
                    "",
                    "",
                    ConfigObjEnabled(),
                    ConfigObjString(
                        "name",
                        "",
                        "Name",
                        "What do you want to call this drive?"
                    ),
                    ConfigObjString(
                        "link",
                        "",
                        "Drive Link",
                        "Adderss of the drive",
                        not_in_config=True,
                        input_attributes=InputAttributes(
                            read_only=True,
                            disabled=True
                        ),
                        value_link=Hardware.disc_drives()
                    ),
                    ConfigObjString(
                        "model",
                        "",
                        "Drive Model",
                        "Adderss of the drive",
                        not_in_config=True,
                        input_attributes=InputAttributes(
                            read_only=True,
                            disabled=True,
                        ),
                        value_link=Hardware.disc_drives()
                    )
                ),
                rules=ConfigRules(for_each=Hardware.disc_drives())
            )
        )

    return config
