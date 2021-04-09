"""video track type information"""
from typing import Optional

from data.video_track_type.base import VideoTrackType


class FeatureTrackType(VideoTrackType):
    """Feature Type"""

    def __init__(
        self, streams: Optional[list] = None, tvshow_link=None, tvshow_special_number=None
    ):
        super().__init__("feature", streams, "Feature")
        self.__tvshow_link = tvshow_link
        self.__tvshow_special_number = tvshow_special_number

    @property
    def tvshow_link(self):
        """return the tv show name for linking"""
        return self.__tvshow_link

    @property
    def tvshow_special_number(self):
        """return the tv show special number"""
        return self.__tvshow_special_number

    def make_dict(self, super_dict: Optional[dict] = None, include_streams: bool = True):
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        if self.__tvshow_link is not None:
            super_dict["tv_show_link"] = self.__tvshow_link
            super_dict["tv_show_special_number"] = self.__tvshow_special_number
        return super().make_dict(super_dict, include_streams)
