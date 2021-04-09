"""video track type information"""
from typing import Optional

from data.video_track_type.base import VideoTrackType


class TrailerTrackType(VideoTrackType):
    """trailer Type"""

    def __init__(self, info: str, streams: Optional[list] = None):
        super().__init__("trailer", streams, f"Trailer: {info}")
        self.__info = info

    @property
    def info(self) -> str:
        """returns trailers movie info"""
        return self.__info

    def make_dict(self, super_dict: Optional[dict] = None, include_streams: bool = True) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["info"] = self.__info
        return super().make_dict(super_dict, include_streams)


class OtherTrackType(VideoTrackType):
    """Other Types"""

    def __init__(self, other_type: str, streams: Optional[list] = None):
        super().__init__("other", streams, f"Other: {other_type}")
        self.__other_type = other_type

    @property
    def other_type(self) -> str:
        """returns other type"""
        return self.__other_type

    def make_dict(self, super_dict: Optional[dict] = None, include_streams: bool = True) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["other_type"] = self.__other_type
        return super().make_dict(super_dict, include_streams)
