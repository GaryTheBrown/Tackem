"""video track type information"""
from typing import Optional

from data.video_track_type.base import VideoTrackType


class EpisodeTrackType(VideoTrackType):
    """Episode Type"""

    def __init__(
        self,
        season: int,
        episode: int,
        streams: Optional[list] = None,
    ):
        super().__init__("episode", streams, f"S{str(season).zfill(2)}E{str(episode).zfill(2)}")
        self.__season = season
        self.__episode = episode

    @property
    def season(self) -> int:
        """returns season number"""
        return self.__season

    @property
    def episode(self) -> int:
        """returns episode number"""
        return self.__episode

    def make_dict(self, super_dict: Optional[dict] = None, include_streams: bool = True) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["season"] = self.__season
        super_dict["episode"] = self.__episode
        return super().make_dict(super_dict, include_streams)
