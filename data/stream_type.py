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

    def json(self) -> str:
        """returns the Stream Type as a Json String"""
        return json.dumps(self.make_dict())

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


class VideoStreamType(StreamType):
    """Other Types"""

    def __init__(self, stream_index: int, label: str = ""):
        super().__init__("video", stream_index, label)

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        return super().make_dict(super_dict)


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
