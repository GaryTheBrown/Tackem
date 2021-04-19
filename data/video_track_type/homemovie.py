"""video track type information"""
from typing import Optional

from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.obj.string import ConfigObjString
from data.video_track_type.base import VideoTrackType


class HomeMovieTrackType(VideoTrackType):
    """Home Movie Types"""

    def __init__(self, name: str):
        super().__init__("Home Movie", f"Home Movie: {name}")
        self.__name = name

    @property
    def name(self) -> str:
        """returns other type"""
        return self.__name

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["name"] = self.__name
        return super().make_dict(super_dict)

    def html_create_data(self, track_id: int, read_only: bool = False) -> dict:
        """returns the data for html"""
        name = ConfigObjString(f"track_{track_id}_name", "", "Track Name", "Enter the track name")
        if read_only:
            name.input_attributes = InputAttributes("readonly")
        name.value = self.name

        return {
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": f"track_{track_id}_type",
                    "value": self.track_type,
                },
                name.html_dict(""),
            ],
        }
