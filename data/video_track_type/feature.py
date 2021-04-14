"""video track type information"""
from typing import Optional

from data.video_track_type.base import VideoTrackType


class FeatureTrackType(VideoTrackType):
    """Feature Type"""

    def __init__(self):
        super().__init__("Feature", "Feature")

    def make_dict(self, super_dict: Optional[dict] = None):
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        return super().make_dict(super_dict)

    def html_create_data(self, track_id: int) -> dict:
        """returns the data for html"""
        return {
            "no_search": False,
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": f"track_{track_id}_type",
                    "value": self.track_type,
                },
            ],
        }
