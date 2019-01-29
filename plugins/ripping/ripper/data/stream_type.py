'''stream type information'''
from abc import ABCMeta, abstractmethod
import json
from libs import html_parts as ghtml_parts
from ..www import html_parts

class StreamType(metaclass=ABCMeta):
    '''Master Type'''
    _types = ["video", "audio", "subtitle"]
    def __init__(self, stream_type, stream_index):
        if stream_type in self._types:
            self._stream_type = stream_type
        self._stream_index = stream_index

    def stream_type(self):
        '''returns the type'''
        return self._stream_type

    def make_dict(self, super_dict=None):
        '''returns the tracks'''
        if super_dict is None:
            super_dict = {}
        super_dict["stream_type"] = self._stream_type
        return super_dict

    def _var_start(self):
        '''returns the variable name start'''
        return "track_%%TRACKINDEX%%_stream_" + str(self._stream_index) + "_"

    @abstractmethod
    def get_edit_panel(self, section_info=""):
        '''returns the edit panel'''
        pass

class VideoStreamType(StreamType):
    '''Other Types'''
    def __init__(self, stream_index, hdr=False):
        super().__init__("video", stream_index)
        self._hdr = hdr
        self._hdr_lock = False
    def hdr(self):
        '''return hdr'''
        return self._hdr

    def check_hdr(self, space, transfer, primaries):
        '''checks and sets the HDR option'''
        if "bt2020" in space and transfer == "smpte2084" and primaries == "bt2020":
            self._hdr = True
            self._hdr_lock = True

    def make_dict(self, super_dict=None):
        '''returns the tracks'''
        if super_dict is None:
            super_dict = {}
        super_dict["hdr"] = self._hdr
        return super().make_dict(super_dict)

    def get_edit_panel(self, section_info=""):
        '''returns the edit panel'''
        self.check_hdr(section_info.get("color_space", ""), section_info.get("color_transfer", ""),
                       section_info.get("color_primaries", ""))
        html = ghtml_parts.hidden(self._var_start() + "type", "video", True)


        resolution = str(section_info.get("width", "???")) + "X"
        resolution += str(section_info.get("height", "???"))
        temp = section_info.get("r_frame_rate", "1/1").split("/")
        frame_rate = str(float(int(temp[0]) / int(temp[1])))
        html = ghtml_parts.quick_table({
            "Codec Name":section_info.get("codec_long_name", ""),
            "Codec Profile":section_info.get("profile", ""),
            "Resolution":resolution,
            "Aspect Ratio":section_info.get("display_aspect_ratio", ""),
            "Frame Rate":frame_rate,
            "Pixel Format":section_info.get("pix_fmt", ""),
            "Colour Space":section_info.get("color_space", ""),
            "Colour Transfer":section_info.get("color_transfer", ""),
            "Colour Primaries":section_info.get("color_primaries", "")
        })
        html += ghtml_parts.item(self._var_start() + "hdr", "HDR",
                                 "Is the Video HDR",
                                 ghtml_parts.checkbox_single("",
                                                             self._var_start() + "hdr",
                                                             self._hdr,
                                                             read_only=self._hdr_lock,
                                                             disabled=self._hdr_lock),
                                 True)
        return html_parts.panel(str(self._stream_index) + ". Video Section", "", html)

class AudioStreamType(StreamType):
    '''Other Types'''
    def __init__(self, stream_index, default=False, dub=False, original=False, comment=False,
                 visual_impaired=False, karaoke=False):
        super().__init__("audio", stream_index)
        self._default = default
        self._dub = dub
        self._original = original
        self._comment = comment
        self._visual_impaired = visual_impaired
        self._karaoke = karaoke

    def default(self):
        '''return default'''
        return self._default

    def dub(self):
        '''return dub'''
        return self._dub

    def original(self):
        '''return original'''
        return self._original

    def comment(self):
        '''return comment'''
        return self._comment

    def visual_impaired(self):
        '''return visual_impaired'''
        return self._visual_impaired

    def karaoke(self):
        '''return karaoke'''
        return self._karaoke

    def make_dict(self, super_dict=None):
        '''returns the tracks'''
        if super_dict is None:
            super_dict = {}
        super_dict["default"] = self._default
        super_dict["dub"] = self._dub
        super_dict["original"] = self._original
        super_dict["comment"] = self._comment
        super_dict["visual_impaired"] = self._visual_impaired
        super_dict["karaoke"] = self._karaoke
        return super().make_dict(super_dict)

    def get_edit_panel(self, section_info=""):
        '''returns the edit panel'''
        html = ghtml_parts.quick_table({
            "Codec Name":section_info.get("codec_long_name", ""),
            "Sample Rate":section_info.get("sample_rate", ""),
            "Channels":section_info.get("channels", ""),
            "Channel Layout":section_info.get("channel_layout", ""),
            "Bit Rate":section_info.get("bit_rate", ""),
            "Language":section_info.get("tags", {}).get("language", ""),
            "Default":section_info.get("disposition", {}).get("default", ""),
            "Dubbed":section_info.get("disposition", {}).get("dub", ""),
            "Original":section_info.get("disposition", {}).get("original", ""),
            "Commentary":section_info.get("disposition", {}).get("comment", ""),
            "Karaoke":section_info.get("disposition", {}).get("karaoke", ""),
            "Visual Impaired":section_info.get("disposition", {}).get("visual_impaired", "")
        })
        html += ghtml_parts.hidden(self._var_start() + "type", "audio", True)
        html += ghtml_parts.item(self._var_start() + "default", "Default Audio",
                                 "Is this the Default Audio Track",
                                 ghtml_parts.checkbox_single("",
                                                             self._var_start() + "default",
                                                             self._default),
                                 True)
        html += ghtml_parts.item(self._var_start() + "dub", "Dubbed Audio",
                                 "Is this a Dubbed Audio Track",
                                 ghtml_parts.checkbox_single("",
                                                             self._var_start() + "dub",
                                                             self._dub),
                                 True)
        html += ghtml_parts.item(self._var_start() + "original", "Original Audio",
                                 "Is this the Original Audio Track",
                                 ghtml_parts.checkbox_single("",
                                                             self._var_start() + "original",
                                                             self._original),
                                 True)
        html += ghtml_parts.item(self._var_start() + "comment", "Comment Audio",
                                 "Is this a Commentary Audio Track",
                                 ghtml_parts.checkbox_single("",
                                                             self._var_start() + "comment",
                                                             self._comment),
                                 True)
        html += ghtml_parts.item(self._var_start() + "visual_impaired", "Visual Impaired Audio",
                                 "Is this a Visual Impaired Audio Track",
                                 ghtml_parts.checkbox_single("",
                                                             self._var_start() + "visual_impaired",
                                                             self._visual_impaired),
                                 True)
        html += ghtml_parts.item(self._var_start() + "karaoke", "Karaoke Audio Track",
                                 "Is this a Karaoke Audio Track",
                                 ghtml_parts.checkbox_single("",
                                                             self._var_start() + "karaoke",
                                                             self._karaoke),
                                 True)
        return html_parts.panel(str(self._stream_index) + ". Audio Section", "", html)

class SubtitleStreamType(StreamType):
    '''Other Types'''
    def __init__(self, stream_index, default=False, forced=False, hearing_impaired=False,
                 lyrics=False):
        super().__init__("subtitle", stream_index)
        self._default = default
        self._forced = forced
        self._hearing_impaired = hearing_impaired
        self._lyrics = lyrics

    def default(self):
        '''return default'''
        return self._default

    def forced(self):
        '''return forced'''
        return self._forced

    def hearing_impaired(self):
        '''return hearing_impaired'''
        return self._hearing_impaired

    def lyrics(self):
        '''return lyrics'''
        return self._lyrics

    def make_dict(self, super_dict=None):
        '''returns the tracks'''
        if super_dict is None:
            super_dict = {}
        super_dict["default"] = self._default
        super_dict["forced"] = self._forced
        super_dict["hearing_impaired"] = self._hearing_impaired
        super_dict["lyrics"] = self._lyrics
        return super().make_dict(super_dict)

    def get_edit_panel(self, section_info=""):
        '''returns the edit panel'''
        html = ghtml_parts.quick_table({
            "Language":section_info.get("tags", {}).get("language", ""),
            "Default":section_info.get("disposition", {}).get("default", ""),
            "Forced":section_info.get("disposition", {}).get("forced", ""),
            "Hearing Impaired":section_info.get("disposition", {}).get("hearing_impaired", ""),
            "Lyrics":section_info.get("disposition", {}).get("lyrics", "")
        })
        html += ghtml_parts.hidden(self._var_start() + "type", "subtitle", True)
        html += ghtml_parts.item(self._var_start() + "default", "Default Subtitle",
                                 "Is this the Default Subtitle Track",
                                 ghtml_parts.checkbox_single("",
                                                             self._var_start() + "default",
                                                             self._default),
                                 True)
        html += ghtml_parts.item(self._var_start() + "forced", "Forced Subtitle",
                                 "Is this a Forced Subtitle Track",
                                 ghtml_parts.checkbox_single("",
                                                             self._var_start() + "forced",
                                                             self._forced),
                                 True)
        html += ghtml_parts.item(self._var_start() + "hearing_impaired",
                                 "Hearing Impaired Subtitle",
                                 "Is this a Hearing Impaired Subtitle Track",
                                 ghtml_parts.checkbox_single("",
                                                             self._var_start() + "hearing_impaired",
                                                             self._hearing_impaired),
                                 True)
        html += ghtml_parts.item(self._var_start() + "lyrics", "Lyrics Track",
                                 "Is this a Lyric Subtitle Track",
                                 ghtml_parts.checkbox_single("",
                                                             self._var_start() + "lyrics",
                                                             self._lyrics),
                                 True)
        return html_parts.panel(str(self._stream_index) + ". Subtitle Section", "", html)

def make_stream_type(stream_index, stream):
    '''transforms the stream returned from the DB or API to the classes above'''
    if isinstance(stream, str):
        stream = json.loads(stream)
    if stream is None:
        return None
    elif stream['type'] == "video":
        return VideoStreamType(stream_index, stream['hdr'])
    elif stream['type'] == "audio":
        return AudioStreamType(stream_index, stream['default'], stream['dub'], stream['original'],
                               stream['comment'], stream['visual_impaired'], stream['karaoke'])
    elif stream['type'] == "subtitle":
        return SubtitleStreamType(stream_index, stream['default'], stream['forced'],
                                  stream['hearing_impaired'], stream['lyrics'])
    return None

def make_blank_stream_type(stream_index, stream_type_code, default=False):
    '''make the blank stream type'''
    if stream_type_code.lower() == "video":
        return VideoStreamType(stream_index)
    elif stream_type_code.lower() == "audio":
        return AudioStreamType(stream_index, default=default)
    elif stream_type_code.lower() == "subtitle":
        return SubtitleStreamType(stream_index, default=default)
    return None
