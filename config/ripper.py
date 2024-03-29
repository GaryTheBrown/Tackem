"""Ripper Config"""
import platform

from config.backend.list import ConfigList
from config.backend.obj.boolean import ConfigObjBoolean
from config.backend.obj.data.checkbox import ConfigObjCheckbox
from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.obj.data.option import ConfigObjOption
from config.backend.obj.data.radio import ConfigObjRadio
from config.backend.obj.enabled import ConfigObjEnabled
from config.backend.obj.integer_number import ConfigObjIntegerNumber
from config.backend.obj.options.checkbox import ConfigObjOptionsCheckBox
from config.backend.obj.options.radio import ConfigObjOptionsRadio
from config.backend.obj.options.select import ConfigObjOptionsSelect
from config.backend.obj.string import ConfigObjString
from config.backend.rules import ConfigRules
from data.audio_format_options import audio_format_options
from data.languages import Languages
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
    "blkid",
    "udfinfo",
]

YES_NO_IA = InputAttributes(data_on="Yes", data_off="No")


def ripper_config() -> ConfigList:
    """Ripper Config"""
    if platform.system() != "Linux":
        return None
    if not check_for_required_programs(RIPPERREQUIREDLINUX, "Ripper"):
        return None

    drives = True
    if not Hardware.disc_drives():
        drives = False
    return ConfigList(
        "ripper",
        "Ripper",
        ConfigObjEnabled(toggle_panel=True),
        ConfigList(
            "drives",
            "Drives",
            ConfigObjEnabled(disabled=drives),
            many_section=ConfigList(
                "",
                "",
                ConfigObjEnabled(),
                ConfigObjString("label", "", "Label", "What do you want to call this drive?"),
                ConfigObjString(
                    "link",
                    "",
                    "Drive Link",
                    "Address of the drive",
                    not_in_config=True,
                    input_attributes=InputAttributes("readonly", "disabled"),
                ),
                ConfigObjString(
                    "uuid",
                    "",
                    "Unique ID",
                    "A Unique code for the drive",
                    not_in_config=True,
                    input_attributes=InputAttributes("read_only", "disabled"),
                ),
                ConfigObjString(
                    "model",
                    "",
                    "Drive Model",
                    "Model of the drive",
                    not_in_config=True,
                    input_attributes=InputAttributes("read_only", "disabled"),
                ),
            ),
            rules=ConfigRules(for_each=Hardware.disc_drives()),
        ),
        ConfigList(
            "iso",
            "ISO",
            ConfigObjEnabled(),
            ConfigObjIntegerNumber(
                "threadcount",
                1,
                "How Many Instances",
                "How Many Instances of MakeMKV do you want to allow at once?",
                input_attributes=InputAttributes(min=1, max=5),
            ),
        ),
        ConfigList(
            "locations",
            "Folder Location",
            ConfigObjString(
                "iso",
                "iso/",
                "ISO Location",
                "Where do you want to watch for ISOs?",
            ),
            ConfigObjString(
                "ripping",
                "ripping/",
                "Ripping Location",
                "Where do you want to store discs while ripping them?",
            ),
        ),
        ConfigList(
            "makemkv",
            "MakeMKV",
            ConfigObjString(
                "key",
                "",
                "Licence Key",
                "Please enter your licence key for makemkv here (restart needed)",
            ),
        ),
        ConfigList(
            "videoripping",
            "Video Ripping",
            ConfigObjOptionsCheckBox(
                "torip",
                [
                    ConfigObjCheckbox("movie", "Movie"),
                    ConfigObjCheckbox("tvshow", "TV Show Episode"),
                    ConfigObjCheckbox("trailer", "Trailer"),
                    ConfigObjCheckbox("extra", "Extra"),
                    ConfigObjCheckbox("other", "Other"),
                ],
                ["movie", "tvshow"],
                "What to Rip",
                "What File Types do you want to rip and include",
            ),
        ),
        ConfigList(
            "audioripping",
            "Audo CD Ripping",
        ),
        ConfigList(
            "converter",
            "Converter",
            ConfigObjEnabled(),
            ConfigObjString(
                "ffmpeglocation",
                "ffmpeg",
                "FFmpeg Location",
                "Where is FFmpeg located?",
            ),
            ConfigObjString(
                "ffprobelocation",
                "ffprobe",
                "FFprobe Location",
                "Where is FFprobe located?",
            ),
            ConfigObjIntegerNumber(
                "threadcount",
                1,
                "How Many Instances?",
                "How Many Threads (Max of 5)",
                input_attributes=InputAttributes(min=1, max=5),
            ),
            ConfigObjOptionsSelect(
                "defaultlanguage",
                Languages.config_option(ConfigObjOption),
                "en",
                "Default Language",
                "What is your main language?",
            ),
            # TODO need to sort this so it can be different for 3D SD HD UHD and HDR Files
            ConfigList(
                "video",
                "Video",
                # VIDEO SECTION
                ConfigObjBoolean(
                    "videoinserttags",
                    True,
                    "Insert Tags",
                    "Do you want to add in the tags to the Video Files?",
                    input_attributes=YES_NO_IA,
                ),
                ConfigObjOptionsSelect(
                    "hdrmode",
                    [
                        ConfigObjOption("keep", "Keep Original"),
                        # ConfigObjOption("x265default", "convert to x265 Default"),
                        # ConfigObjOption("x265custom", "convert to x265 Custom")
                    ],
                    "keep",
                    "HDR Mode",
                    "How to treat HDR videos",
                ),
                ConfigObjOptionsSelect(
                    "video3dtype",
                    [
                        ConfigObjOption("keep", "Keep Original"),
                        ConfigObjOption("sbsl", "Side by Side (Left Eye First)"),
                        ConfigObjOption("sbsr", "Side by Side (Right Eye First)"),
                        ConfigObjOption("sbs2l", "Half Side by Side (Left Eye First)"),
                        ConfigObjOption("sbs2r", "Half Side by Side (Right Eye First)"),
                        ConfigObjOption("abl", "Top Bottom (Left Eye Top)"),
                        ConfigObjOption("abr", "Top Bottom (Right Eye Top)"),
                        ConfigObjOption("ab2l", "Half Top Bottom (Left Eye Top)"),
                        ConfigObjOption("ab2r", "Half Top Bottom (Right Eye Top)"),
                        ConfigObjOption("al", "Alternating Frames (Left Eye First)"),
                        ConfigObjOption("ar", "Alternating Frames (Right Eye First)"),
                        ConfigObjOption("irl", "Interleaved Rows (Left Eye Has Top Row)"),
                        ConfigObjOption("irr", "Interleaved Rows (Right Eye Has Top Row)"),
                        ConfigObjOption("arbg", "Anaglyph Red/Blue Grayscale"),
                        ConfigObjOption("argg", "Anaglyph Red/Green Grayscale"),
                        ConfigObjOption("arcg", "Anaglyph Red/Cyan Grayscale"),
                        ConfigObjOption("arch", "Anaglyph Red/Cyan Half Coloured"),
                        ConfigObjOption("arcc", "Anaglyph Red/Cyan Colour"),
                        ConfigObjOption("arcd", "Anaglyph Red/Cyan Colour dubois"),
                        ConfigObjOption("agmg", "Anaglyph Green/Magenta Grayscale"),
                        ConfigObjOption("agmh", "Anaglyph Green/Magenta Half Coloured"),
                        ConfigObjOption("agmc", "Anaglyph Green/Magenta Coloured"),
                        ConfigObjOption("agmd", "Anaglyph Green/Magenta Colour Dubois"),
                        ConfigObjOption("aybg", "Anaglyph Yellow/Blue Grayscale"),
                        ConfigObjOption("aybh", "Anaglyph Yellow/Blue Half Coloured"),
                        ConfigObjOption("aybc", "Anaglyph Yellow/Blue Coloured"),
                        ConfigObjOption("aybd", "Anaglyph Yellow/Blue Colour Dubois"),
                        ConfigObjOption("ml", "Mono Output (Left Eye Only)"),
                        ConfigObjOption("mr", "Mono Output (Right Eye Only)"),
                        ConfigObjOption("chl", "Checkerboard (Left Eye First)"),
                        ConfigObjOption("chr", "Checkerboard (Right Eye First)"),
                        ConfigObjOption("icl", "Interleaved Columns (Left Eye First)"),
                        ConfigObjOption("icr", "Interleaved Columns (Right Eye First)"),
                        ConfigObjOption("hdmi", "HDMI Frame Pack"),
                    ],
                    "keep",
                    "3D Type",
                    "what 3D mode do you want to transform 3d Discs into",
                ),
                ConfigObjOptionsSelect(
                    "videoresolution",
                    [
                        ConfigObjOption("keep", "Keep Original"),
                        ConfigObjOption("2160", "4K"),
                        ConfigObjOption("1080", "1080"),
                        ConfigObjOption("720", "720"),
                        ConfigObjOption("sd", "SD"),
                    ],
                    "keep",
                    "Max Video Resolution",
                    "What is the maximum resolution you want to keep or downscale to?",
                ),
                ConfigObjOptionsRadio(
                    "videocodec",
                    [
                        ConfigObjRadio(
                            "keep",
                            "Keep Original",
                            input_attributes=InputAttributes(
                                data_click_hide=[
                                    "ripper_converter_video_videopreset",
                                    "ripper_converter_video_x26custom_section",
                                ]
                            ),
                        ),
                        ConfigObjRadio(
                            "x264default",
                            "X264 Default",
                            input_attributes=InputAttributes(
                                data_click_hide=[
                                    "ripper_converter_video_videopreset",
                                    "ripper_converter_video_x26custom_section",
                                ]
                            ),
                        ),
                        ConfigObjRadio(
                            "x265default",
                            "X265 Default",
                            input_attributes=InputAttributes(
                                data_click_hide=[
                                    "ripper_converter_video_videopreset",
                                    "ripper_converter_video_x26custom_section",
                                ]
                            ),
                        ),
                        ConfigObjRadio(
                            "x264custom",
                            "X264 Custom",
                            input_attributes=InputAttributes(
                                data_click_show="ripper_converter_video_x26custom_section",
                                data_click_hide="ripper_converter_video_videopreset",
                            ),
                        ),
                        ConfigObjRadio(
                            "x265custom",
                            "X265 Custom",
                            input_attributes=InputAttributes(
                                data_click_show="ripper_converter_video_x26custom_section",
                                data_click_hide="ripper_converter_video_videopreset",
                            ),
                        ),
                        ConfigObjRadio(
                            "preset",
                            "Preset (choose from a list)",
                            input_attributes=InputAttributes(
                                data_click_show="ripper_converter_video_videopreset",
                                data_click_hide="ripper_converter_video_x26custom_section",
                            ),
                        ),
                    ],
                    "keep",
                    "Video Codec",
                    "What video codec do you wish to convert to?",
                ),
                ConfigObjOptionsSelect(
                    "videopreset",
                    video_presets_config_options(ConfigObjOption),
                    "",
                    "Video Preset",
                    "What preset do you want to use?",
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
                        input_attributes=InputAttributes(min=0, max=51),
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
                        ),
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
                            ConfigObjOption("veryslow", "Very Slow"),
                        ],
                        "medium",
                        "Preset",
                        """
A preset is a collection of options that will provide a certain encoding speed to compression ratio.
A slower preset will provide better compression (compression is quality per filesize).
This means that, for example, if you target a certain file size or constant bit rate,
you will achieve better quality with a slower preset. Similarly, for constant quality encoding,
you will simply save bitrate by choosing a slower preset.
Use the slowest preset that you have patience for.""",
                    ),
                    ConfigObjString("x26extra", "", "Extra commands", "Other commands?"),
                    is_section=True,
                ),
            ),
            ConfigList(
                "audio",
                "Audio",
                # AUDIO SECTION
                ConfigObjOptionsRadio(
                    "originalordub",
                    [
                        ConfigObjRadio("original", "Original"),
                        ConfigObjRadio("dub", "Dubbed"),
                    ],
                    "all",
                    "Original or Dubbed Language",
                    """
Do you want the default stream to be the Original language or dubbed in your language if available?
""",
                ),
                ConfigObjOptionsRadio(
                    "audiolanguage",
                    [
                        ConfigObjRadio(
                            "all",
                            "All",
                            input_attributes=InputAttributes(
                                data_click_hide="ripper_converter_audio_audiolanglist_section"
                            ),
                        ),
                        ConfigObjRadio(
                            "original",
                            "Original Language Only",
                            input_attributes=InputAttributes(
                                data_click_hide="ripper_converter_audio_audiolanglist_section"
                            ),
                        ),
                        ConfigObjRadio(
                            "default",
                            "Default Language Only",
                            input_attributes=InputAttributes(
                                data_click_hide="ripper_converter_audio_audiolanglist_section"
                            ),
                        ),
                        ConfigObjRadio(
                            "deaultandoriginal",
                            "Original Language + Default Language",
                            input_attributes=InputAttributes(
                                data_click_hide="ripper_converter_audio_audiolanglist_section"
                            ),
                        ),
                        ConfigObjRadio(
                            "selectedandoriginal",
                            "Original Language + Selected Languages",
                            input_attributes=InputAttributes(
                                data_click_show="ripper_converter_audio_audiolanglist_section"
                            ),
                        ),
                        ConfigObjRadio(
                            "selected",
                            "Selected Languages",
                            input_attributes=InputAttributes(
                                data_click_show="ripper_converter_audio_audiolanglist_section"
                            ),
                        ),
                    ],
                    "all",
                    "Audio Languages",
                    "What Audio Languages do you want to keep?",
                ),
                ConfigList(
                    "audiolanglist",
                    "Audio Language List",
                    ConfigObjOptionsCheckBox(
                        "audiolanguages",
                        Languages.config_option(ConfigObjCheckbox),
                        "en",
                        "Audio Languages",
                        "",
                    ),
                    is_section=True,
                ),
                ConfigObjOptionsRadio(
                    "audioformat",
                    [
                        ConfigObjRadio(
                            "all",
                            "All",
                            input_attributes=InputAttributes(
                                data_click_hide="ripper_converter_audio_audioformatlist_section"
                            ),
                        ),
                        ConfigObjRadio(
                            "highest",
                            "Highest Quality",
                            input_attributes=InputAttributes(
                                "disabled",
                                data_click_hide="ripper_converter_audio_audioformatlist_section",
                            ),
                        ),
                        ConfigObjRadio(
                            "selected",
                            "Selected Formats",
                            input_attributes=InputAttributes(
                                data_click_show="ripper_converter_audio_audioformatlist_section"
                            ),
                        ),
                    ],
                    "all",
                    "Audio Format",
                    "What Audio Formats do you want to keep?",
                ),
                ConfigList(
                    "audioformatlist",
                    "Audio Format List",
                    ConfigObjOptionsCheckBox(
                        "audioformats",
                        audio_format_options(ConfigObjCheckbox),
                        "",
                        "Audio Formats",
                        "",
                    ),
                    is_section=True,
                ),
            ),
            ConfigList(
                "chapters",
                "Chapters",
                # CHAPTERS SECTION
                ConfigObjBoolean(
                    "keepchapters",
                    True,
                    "Keep Chapters",
                    "Do you want to keep the chapter points?",
                    input_attributes=YES_NO_IA,
                ),
            ),
            ConfigList(
                "subtitles",
                "Subtitles",
                # SUBTITLES SECTION
                ConfigObjOptionsRadio(
                    "subtitle",
                    [
                        ConfigObjRadio(
                            "all",
                            "All",
                            input_attributes=InputAttributes(
                                data_click_hide="ripper_converter_subtitles_subtitleslist_section"
                            ),
                        ),
                        ConfigObjRadio(
                            "none",
                            "None",
                            input_attributes=InputAttributes(
                                data_click_hide="ripper_converter_subtitles_subtitleslist_section"
                            ),
                        ),
                        ConfigObjRadio(
                            "original",
                            "Original Language Only",
                            input_attributes=InputAttributes(
                                data_click_hide="ripper_converter_subtitles_subtitleslist_section"
                            ),
                        ),
                        ConfigObjRadio(
                            "default",
                            "Default Language Only",
                            input_attributes=InputAttributes(
                                data_click_hide="ripper_converter_subtitles_subtitleslist_section"
                            ),
                        ),
                        ConfigObjRadio(
                            "deaultandoriginal",
                            "Original Language + Default Language",
                            input_attributes=InputAttributes(
                                data_click_hide="ripper_converter_subtitles_subtitleslist_section"
                            ),
                        ),
                        ConfigObjRadio(
                            "selectedandoriginal",
                            "Original Language + Selected Languages",
                            input_attributes=InputAttributes(
                                data_click_show="ripper_converter_subtitles_subtitleslist_section"
                            ),
                        ),
                        ConfigObjRadio(
                            "selected",
                            "Selected Languages",
                            input_attributes=InputAttributes(
                                data_click_show="ripper_converter_subtitles_subtitleslist_section"
                            ),
                        ),
                    ],
                    "all",
                    "Subtitles",
                    "What subtitles do you want to keep?",
                ),
                ConfigList(
                    "subtitleslist",
                    "Subtitle List",
                    ConfigObjOptionsCheckBox(
                        "subtitlelanguages",
                        Languages.config_option(ConfigObjCheckbox),
                        "",
                        "Subtitle Languages",
                        "",
                    ),
                    is_section=True,
                ),
                ConfigObjBoolean(
                    "keepclosedcaptions",
                    True,
                    "Keep Closed Captions",
                    "Do you want to keep the closed captions?",
                    input_attributes=YES_NO_IA,
                ),
            ),
        ),
    )
