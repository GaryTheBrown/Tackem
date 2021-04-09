"""disc type information"""
from typing import List
from typing import Optional

from data.disc_type.base import DiscType
from libs.config.obj.data.button import Button
from libs.config.obj.string import ConfigObjString


class DocumentaryDiscType(DiscType):
    """Documentary Disc Type"""

    _track_types: List[str] = ["dontrip", "feature", "episode", "trailer", "extra"]

    def __init__(self, name: str, tracks: list, language: str = "eng"):
        super().__init__("Documentary", name, tracks, language, None)

    def make_dict(self, super_dict: Optional[dict] = None, no_tracks: bool = False) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        return DiscType.make_dict(self, super_dict, no_tracks)

    def track_title(self, index: int):
        """generates the title for the track"""
        return f"{self.name.capitalize()} - {self.tracks[index].title}"

    def html_search_data(self) -> dict:
        """returns the data for html"""
        name = ConfigObjString(
            "name",
            "",
            "Documentary Name",
            "Enter the name of the Documentary here",
            button=Button("Search By Title", "docSearch", True, item_width=175),
        )
        name.value = self.name

        imdbid = ConfigObjString(
            "imbbid",
            "",
            "IMDB ID",
            "Enter the IMDB ID here",
            button=Button("Search By IMDB ID", "docSearchIMDBid", True, item_width=175),
        )

        tvdbid = ConfigObjString(
            "tvdbid",
            "",
            "TVDB ID",
            "Enter the TVDB ID here",
            button=Button("Search By TVDB ID", "docSearchTVDBid", True, item_width=175),
        )

        tmdbid = ConfigObjString(
            "tmbbid",
            "",
            "TMDB ID",
            "Enter the TMDB ID here",
            button=Button("Search By TMDB ID", "docSearchTMDBid", True, item_width=175),
        )

        return {
            "no_search": False,
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": "disc_type",
                    "value": self.disc_type,
                },
                name.html_dict(""),
                imdbid.html_dict(""),
                tvdbid.html_dict(""),
                tmdbid.html_dict(""),
            ],
        }
