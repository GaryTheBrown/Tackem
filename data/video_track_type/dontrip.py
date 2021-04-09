"""video track type information"""
from typing import Optional

from data.video_track_type.base import VideoTrackType


class DONTRIPTrackType(VideoTrackType):
    """Other Types"""

    def __init__(self, reason: str):
        super().__init__("dontrip", None, "DON'T RIP ME")
        self.__reason = reason

    @property
    def reason(self) -> str:
        """return the reason not to rip this track"""
        return self.__reason

    def make_dict(self, super_dict: Optional[dict] = None, include_streams: bool = True) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["reason"] = self.__reason
        return super().make_dict(super_dict, include_streams)
