"""stream type information"""
from typing import Optional

from data.stream_type.base import StreamType


class VideoStreamType(StreamType):
    """Other Types"""

    def __init__(self, stream_index: int, label: str = ""):
        super().__init__("video", stream_index, label)

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        return super().make_dict(super_dict)
