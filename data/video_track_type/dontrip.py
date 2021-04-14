"""video track type information"""
from typing import Optional

from data.video_track_type.base import VideoTrackType
from libs.config.obj.string import ConfigObjString


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

    def html_create_data(self, track_id: int) -> dict:
        """returns the data for html"""
        reason = ConfigObjString(
            f"track_{track_id}_reason", "", "Reason", "Enter the reason to not rip this at all here"
        )
        reason.value = self.reason

        return {
            "no_search": False,
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": f"track_{track_id}_type",
                    "value": self.track_type,
                },
                reason.html_dict(""),
            ],
        }
