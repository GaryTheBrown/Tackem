"""stream type information"""
import json
from abc import ABCMeta
from typing import Optional


class StreamType(metaclass=ABCMeta):
    """Master Type"""

    _types = ["video", "audio", "subtitle"]

    def __init__(self, stream_type: str, stream_index: int, label: str):
        self.__stream_type = stream_type if stream_type in self._types else ""
        self.__stream_index = stream_index
        self.__label = label

    @property
    def stream_type(self) -> str:
        """returns the type"""
        return self.__stream_type

    @property
    def stream_index(self) -> int:
        """returns the index"""
        return self.__stream_index

    @property
    def label(self) -> str:
        """return label"""
        return self.__label

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["stream_type"] = self.__stream_type
        super_dict["label"] = self.__label
        return super_dict

    @property
    def _var_start(self) -> str:
        """returns the variable name start"""
        return "track_%%TRACKINDEX%%_stream_" + str(self.__stream_index) + "_"

    # @abstractmethod
    # def get_edit_panel(self, section_info: str = "") -> str:
    #     '''returns the edit panel'''


class VideoStreamType(StreamType):
    """Other Types"""

    def __init__(self, stream_index: int, label: str = ""):
        super().__init__("video", stream_index, label)

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        return super().make_dict(super_dict)

    # def get_edit_panel(self, section_info=""):
    #     '''returns the edit panel'''
    #     ffprobeinfo = {}
    #     if isinstance(section_info, dict):
    #         resolution = str(section_info.get("width", "???")) + "X"
    #         resolution += str(section_info.get("height", "???"))
    #         temp = section_info.get("r_frame_rate", "1/1").split("/")
    #         frame_rate = str(float(int(temp[0]) / int(temp[1])))
    #         ffprobeinfo = {
    #             "Codec Name": section_info.get("codec_long_name", ""),
    #             "Codec Profile": section_info.get("profile", ""),
    #             "Resolution": resolution,
    #             "Aspect Ratio": section_info.get("display_aspect_ratio", ""),
    #             "Frame Rate": frame_rate,
    #             "Pixel Format": section_info.get("pix_fmt", ""),
    #             "Colour Space": section_info.get("color_space", ""),
    #             "Colour Transfer": section_info.get("color_transfer", ""),
    #             "Colour Primaries": section_info.get("color_primaries", "")
    #         }
    #     html = ghtml_parts.hidden(
    #         self._var_start + "stream_type", "video", True)
    #     html += ghtml_parts.item(self._var_start + "label", "Label",
    #                              "Label of the Subtitles",
    #                              ghtml_parts.input_box("text", self._var_start + "label",
    #                                                    self._label),
    #                              True)
    #     stream_panel_html = html_parts.video_stream_panel(ffprobeinfo, html)
    #     return html_parts.video_panel(str(self._stream_index) + ". Video Section", "",
    #                                   stream_panel_html)


class AudioStreamType(StreamType):
    """Other Types"""

    def __init__(
        self,
        stream_index: int,
        dub: bool = False,
        original: bool = False,
        comment: bool = False,
        visual_impaired: bool = False,
        karaoke: bool = False,
        label: str = "",
        duplicate: bool = False,
    ):
        super().__init__("audio", stream_index, label)
        self.__dub = dub
        self.__original = original
        self.__comment = comment
        self.__visual_impaired = visual_impaired
        self.__karaoke = karaoke
        self.__duplicate = duplicate

    @property
    def dub(self) -> bool:
        """return dub"""
        return self.__dub

    @property
    def original(self) -> bool:
        """return original"""
        return self.__original

    @property
    def comment(self) -> bool:
        """return comment"""
        return self.__comment

    @property
    def visual_impaired(self) -> bool:
        """return visual_impaired"""
        return self.__visual_impaired

    @property
    def karaoke(self) -> bool:
        """return karaoke"""
        return self.__karaoke

    @property
    def duplicate(self) -> bool:
        """return if duplicate stream"""
        return self.__duplicate

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["dub"] = self.__dub
        super_dict["original"] = self.__original
        super_dict["comment"] = self.__comment
        super_dict["visual_impaired"] = self.__visual_impaired
        super_dict["karaoke"] = self.__karaoke
        super_dict["duplicate"] = self.__duplicate
        return super().make_dict(super_dict)

    # def get_edit_panel(self, section_info=""):
    #     '''returns the edit panel'''
    #     ffprobeinfo = {}
    #     if isinstance(section_info, dict):
    #         language_3t = section_info.get("tags", {}).get("language", "")
    #         language = Languages().get_name_from_3t(language_3t)
    #         ffprobeinfo = {
    #             "Codec Name": section_info.get("codec_long_name", ""),
    #             "Sample Rate": "{:,}".format(
    #                 int(section_info.get("sample_rate", 0)) / 1000) + "kHz",
    #             "Channels": section_info.get("channels", ""),
    #             "Channel Layout": section_info.get("channel_layout", ""),
    #             "Bit Rate": "{:,}".format(int(section_info.get("bit_rate", 0)) / 1000) + "kbit/s",
    #             "Language": language,
    #             "Default": bool(section_info.get("disposition", {}).get("default", "")),
    #             "Dubbed": bool(section_info.get("disposition", {}).get("dub", "")),
    #             "Original": bool(section_info.get("disposition", {}).get("original", "")),
    #             "Commentary": bool(section_info.get("disposition", {}).get("comment", "")),
    #             "Karaoke": bool(section_info.get("disposition", {}).get("karaoke", "")),
    #             "Visual Impaired": bool(section_info.get("disposition", {}).get("visual_impaired",
    #                                                                             ""))
    #         }
    #     html = ghtml_parts.hidden(
    #         self._var_start + "stream_type", "audio", True)
    #     html += html_parts.video_item(self._var_start + "dub", "Dubbed Audio",
    #                                   "Is this a Dubbed Audio Track",
    #                                   ghtml_parts.checkbox_single("",
    #                                                               self._var_start + "dub",
    #                                                               self._dub),
    #                                   True)
    #     html += html_parts.video_item(self._var_start + "original", "Original Audio",
    #                                   "Is this the Original Audio Track",
    #                                   ghtml_parts.checkbox_single("",
    #                                                               self._var_start + "original",
    #                                                               self._original),
    #                                   True)
    #     html += html_parts.video_item(self._var_start + "comment", "Comment Audio",
    #                                   "Is this a Commentary Audio Track",
    #                                   ghtml_parts.checkbox_single("",
    #                                                               self._var_start + "comment",
    #                                                               self._comment),
    #                                   True)
    #     tmp_label = self._var_start + "visual_impaired"
    #     html += html_parts.video_item(self._var_start + "visual_impaired",
    #                                   "Visual Impaired Audio",
    #                                   "Is this a Visual Impaired Audio Track",
    #                                   ghtml_parts.checkbox_single("",
    #                                                               tmp_label,
    #                                                               self._visual_impaired),
    #                                   True)
    #     html += html_parts.video_item(self._var_start + "karaoke", "Karaoke Audio Track",
    #                                   "Is this a Karaoke Audio Track",
    #                                   ghtml_parts.checkbox_single("",
    #                                                               self._var_start + "karaoke",
    #                                                               self._karaoke),
    #                                   True)
    #     html += html_parts.video_item(self._var_start + "duplicate", "Duplicate",
    #                                   "Is this a Duplicate Audio Track?",
    #                                   ghtml_parts.checkbox_single("",
    #                                                               self._var_start + "duplicate",
    #                                                               self._duplicate),
    #                                   True)
    #     html += ghtml_parts.item(self._var_start + "label", "Label",
    #                              "Label of the Subtitles",
    #                              ghtml_parts.input_box("text", self._var_start + "label",
    #                                                    self._label),
    #                              True)
    #     stream_panel_html = html_parts.video_stream_panel(ffprobeinfo, html)
    #     return html_parts.video_panel(str(self._stream_index) + ". Audio Section", "",
    #                                   stream_panel_html)


class SubtitleStreamType(StreamType):
    """Other Types"""

    def __init__(
        self,
        stream_index: int,
        forced: bool = False,
        hearing_impaired: bool = False,
        lyrics: bool = False,
        label: str = "",
        duplicate: bool = False,
        comment: bool = False,
    ):
        super().__init__("subtitle", stream_index, label)
        self.__forced = forced
        self.__hearing_impaired = hearing_impaired
        self.__comment = comment
        self.__lyrics = lyrics
        self.__duplicate = duplicate

    @property
    def forced(self) -> bool:
        """return forced"""
        return self.__forced

    @property
    def hearing_impaired(self) -> bool:
        """return hearing_impaired"""
        return self.__hearing_impaired

    @property
    def comment(self) -> bool:
        """return comment"""
        return self.__comment

    @property
    def lyrics(self) -> bool:
        """return lyrics"""
        return self.__lyrics

    @property
    def duplicate(self) -> bool:
        """return if duplicate"""
        return self.__duplicate

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["forced"] = self.__forced
        super_dict["hearing_impaired"] = self.__hearing_impaired
        super_dict["comment"] = self.__comment
        super_dict["lyrics"] = self.__lyrics
        super_dict["duplicate"] = self.__duplicate
        return super().make_dict(super_dict)

    # def get_edit_panel(self, section_info=""):
    #     '''returns the edit panel'''
    #     ffprobeinfo = {}
    #     if isinstance(section_info, dict):
    #         language_3t = section_info.get("tags", {}).get("language", "")
    #         language = Languages().get_name_from_3t(language_3t)
    #         ffprobeinfo = {
    #             "Language": language,
    #             "Default": bool(section_info.get("disposition", {}).get("default", "")),
    #             "Forced": bool(section_info.get("disposition", {}).get("forced", "")),
    #             "Hearing Impaired":bool(section_info.get("disposition",{}).get("hearing_impaired",
    #                                                                              "")),
    #             "Commentary": bool(section_info.get("disposition", {}).get("comment", "")),
    #             "Lyrics": bool(section_info.get("disposition", {}).get("lyrics", ""))
    #         }

    #     html = ghtml_parts.hidden(
    #         self._var_start + "stream_type", "subtitle", True)
    #     html += html_parts.video_item(self._var_start + "forced", "Forced Subtitle",
    #                                   "Is this a Forced Subtitle Track",
    #                                   ghtml_parts.checkbox_single("",
    #                                                               self._var_start + "forced",
    #                                                               self._forced),
    #                                   True)
    #     tmp_variable = self._var_start + "hearing_impaired"
    #     html += html_parts.video_item(self._var_start + "hearing_impaired",
    #                                   "Hearing Impaired Subtitle",
    #                                   "Is this a Hearing Impaired Subtitle Track",
    #                                   ghtml_parts.checkbox_single("",
    #                                                               tmp_variable,
    #                                                               self._hearing_impaired),
    #                                   True)
    #     html += html_parts.video_item(self._var_start + "lyrics", "Lyrics Track",
    #                                   "Is this a Lyric Subtitle Track",
    #                                   ghtml_parts.checkbox_single("",
    #                                                               self._var_start + "lyrics",
    #                                                               self._lyrics),
    #                                   True)
    #     html += html_parts.video_item(self._var_start + "comment", "Comment Track",
    #                                   "Is this a Commentary Subtitle Track",
    #                                   ghtml_parts.checkbox_single("",
    #                                                               self._var_start + "comment",
    #                                                               self._comment),
    #                                   True)
    #     html += html_parts.video_item(self._var_start + "duplicate", "Duplicate",
    #                                   "Is this a Duplicate Subtitle Track?",
    #                                   ghtml_parts.checkbox_single("",
    #                                                               self._var_start + "duplicate",
    #                                                               self._duplicate),
    #                                   True)
    #     html += ghtml_parts.item(self._var_start + "label", "Label",
    #                              "Label of the Subtitles",
    #                              ghtml_parts.input_box("text", self._var_start + "label",
    #                                                    self._label),
    #                              True)
    #     stream_panel_html = html_parts.video_stream_panel(ffprobeinfo, html)
    #     return html_parts.video_panel(str(self._stream_index) + ". Subtitle Section", "",
    #                                   stream_panel_html)


def make_stream_type(stream_index: int, stream: str) -> StreamType:
    """transforms the stream returned from the DB or API to the classes above"""
    if isinstance(stream, str):
        stream = json.loads(stream)
    for key in stream:
        if stream[key] == "True":
            stream[key] = True
        if stream[key] == "False":
            stream[key] = False
    if stream is None:
        return None
    elif stream["stream_type"] == "video":
        return VideoStreamType(stream_index)
    elif stream["stream_type"] == "audio":
        return AudioStreamType(
            stream_index,
            dub=stream.get("dub", False),
            original=stream.get("original", False),
            comment=stream.get("comment", False),
            visual_impaired=stream.get("visual_impaired", False),
            karaoke=stream.get("karaoke", False),
            label=stream.get("label", ""),
            duplicate=stream.get("duplicate", ""),
        )
    elif stream["stream_type"] == "subtitle":
        return SubtitleStreamType(
            stream_index,
            forced=stream.get("forced", False),
            hearing_impaired=stream.get("hearing_impaired", False),
            lyrics=stream.get("lyrics", False),
            label=stream.get("label", ""),
            duplicate=stream.get("duplicate", False),
            comment=stream.get("comment", False),
        )
    return None


def make_blank_stream_type(stream_index: int, stream_type_code: str) -> StreamType:
    """make the blank stream type"""
    if stream_type_code.lower() == "video":
        return VideoStreamType(stream_index)
    elif stream_type_code.lower() == "audio":
        return AudioStreamType(stream_index)
    elif stream_type_code.lower() == "subtitle":
        return SubtitleStreamType(stream_index)
    return None
