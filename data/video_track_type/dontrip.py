"""video track type information"""
from typing import Optional

from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.obj.string import ConfigObjString
from data.video_track_type.base import VideoTrackType


class DONTRIPTrackType(VideoTrackType):
    """Other Types"""

    def __init__(self, reason: str):
        super().__init__("Dont Rip", "DON'T RIP ME")
        self.__reason = reason

    @property
    def reason(self) -> str:
        """return the reason not to rip this track"""
        return self.__reason

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["reason"] = self.__reason
        return super().make_dict(super_dict)

    def html_create_data(self, track_id: int, read_only: bool = False) -> dict:
        """returns the data for html"""
        reason = ConfigObjString(
            f"track_{track_id}_reason", "", "Reason", "Enter the reason to not rip this at all here"
        )
        if read_only:
            reason.input_attributes = InputAttributes("readonly")

        reason.value = self.reason

        return {
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": f"track_{track_id}_type",
                    "value": self.track_type,
                },
                reason.html_dict(""),
            ],
        }
