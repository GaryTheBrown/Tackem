"""disc type information"""
from typing import List
from typing import Optional

from data.disc_type.base import DiscType
from libs.config.obj.string import ConfigObjString


class HomeMovieDiscType(DiscType):
    """HomeMovie Disc Type"""

    _track_types: List[str] = ["dontrip", "feature"]

    def __init__(self, name: str, info: str, tracks: list, language: str = "eng"):
        super().__init__("HomeMovie", name, tracks, language, None)
        self.__info = info

    @property
    def info(self) -> str:
        """returns the temp info"""
        return self.__info

    def make_dict(self, super_dict: Optional[dict] = None, no_tracks: bool = False) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        return DiscType.make_dict(self, super_dict, no_tracks)

    def track_title(self, index: int):
        """generates the title for the track"""
        return f"Home Movie {self.name.capitalize()} - {self.tracks[index].title}"

    def html_search_data(self) -> dict:
        """returns the data for html"""
        name = ConfigObjString(
            "name",
            "",
            "Disc Name",
            "Enter the name of the Disc here",
        )

        return {
            "no_search": True,
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": "disc_type",
                    "value": self.disc_type,
                },
                name.html_dict(""),
            ],
        }
