"""video track type information"""
from typing import Optional

from data.video_track_type.base import VideoTrackType
from libs.config.obj.integer_number import ConfigObjIntegerNumber


class EpisodeTrackType(VideoTrackType):
    """Episode Type"""

    def __init__(self, season: int, episode: int):
        super().__init__("Episode", f"S{str(season).zfill(2)}E{str(episode).zfill(2)}")
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

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["season"] = self.__season
        super_dict["episode"] = self.__episode
        return super().make_dict(super_dict)

    def html_create_data(self, track_id: int) -> dict:
        """returns the data for html"""
        season = ConfigObjIntegerNumber(
            f"track_{track_id}_season", 1, "Season", "Enter the season Number (0 for specials)"
        )
        season.value = self.season

        episode = ConfigObjIntegerNumber(
            f"track_{track_id}_episode", 1, "Episode", "Enter the episode Number"
        )
        episode.value = self.episode
        return {
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": f"track_{track_id}_type",
                    "value": self.track_type,
                },
                season.html_dict(""),
                episode.html_dict(""),
            ],
        }
