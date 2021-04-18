"""video track type information"""
from typing import Optional

from config.backend.obj.string import ConfigObjString
from data.video_track_type.base import VideoTrackType


class TrailerTrackType(VideoTrackType):
    """trailer Type"""

    def __init__(self, name: str):
        super().__init__("Trailer", f"Trailer: {name}")
        self.__name = name

    @property
    def name(self) -> str:
        """returns trailers movie name"""
        return self.__name

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["name"] = self.__name
        return super().make_dict(super_dict)

    def html_create_data(self, track_id: int) -> dict:
        """returns the data for html"""
        name = ConfigObjString(
            f"track_{track_id}_name", "", "Trailer Name", "Enter the trailer name"
        )
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
