"""disc type information"""
from typing import List
from typing import Optional

from data.disc_type.base import DiscType
from libs.config.obj.data.button import Button
from libs.config.obj.string import ConfigObjString


class TVShowDiscType(DiscType):
    """TV Show Disc Type"""

    _track_types: List[str] = ["dontrip", "episode", "trailer", "extra"]

    def __init__(
        self,
        name: str,
        tvdbid: str,
        tracks: list,
        language: str = "eng",
        moviedbid="",
    ):
        super().__init__("TV Show", name, tracks, language, moviedbid)
        self.__tvdbid = tvdbid

    @property
    def tvdbid(self) -> str:
        """returns TV Show name"""
        return self.__tvdbid

    def make_dict(self, super_dict: Optional[dict] = None, no_tracks: bool = False) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["tvdbid"] = self.__tvdbid
        return DiscType.make_dict(self, super_dict, no_tracks)

    def track_title(self, index: int):
        """generates the title for the track"""
        return f"{self.name.capitalize()} - {self.tracks[index].title}"

    def html_search_data(self) -> dict:
        """returns the data for html"""
        name = ConfigObjString(
            "name",
            "",
            "TV Show Name",
            "Enter the name of the TV Show here",
            button=Button("Search By Title", "tvSearch", True, item_width=175),
        )
        name.value = self.name

        tvdbid = ConfigObjString(
            "tvdbid",
            "",
            "TVDB ID",
            "Enter the TVDB ID here",
            button=Button("Search By TVDB ID", "tvSearchTVDBid", True, item_width=175),
        )
        tvdbid.value = self.tvdbid

        tmdbid = ConfigObjString(
            "tmbbid",
            "",
            "TMDB ID",
            "Enter the TMDB ID here",
            button=Button("Search By TMDB ID", "tvSearchTMDBid", True, item_width=175),
        )
        tmdbid.value = self.moviedbid

        return {
            "no_search": False,
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": "disc_type",
                    "value": self.disc_type,
                },
                name.html_dict(""),
                tvdbid.html_dict(""),
                tmdbid.html_dict(""),
            ],
        }
