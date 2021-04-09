"""video track type information"""
from typing import Optional

from data.video_track_type.base import VideoTrackType


class ExtraTrackType(VideoTrackType):
    """Extra Type"""

    def __init__(self, name: str, streams: Optional[list] = None):
        super().__init__("extra", streams, f"Extra: {name}")
        self.__name = name

    @property
    def name(self) -> str:
        """returns extra name"""
        return self.__name

    def make_dict(self, super_dict: Optional[dict] = None, include_streams: bool = True) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["name"] = self.__name
        return super().make_dict(super_dict, include_streams)
