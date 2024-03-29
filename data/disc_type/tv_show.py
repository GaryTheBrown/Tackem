"""disc type information"""
from typing import List
from typing import Optional

from config.backend.obj.data.button import Button
from config.backend.obj.string import ConfigObjString
from data.disc_type.base import DiscType
from libs.scraper import Scraper


class TVShowDiscType(DiscType):
    """TV Show Disc Type"""

    _track_types: List[str] = ["Dont Rip", "Episode", "Trailer", "Extra"]

    def __init__(
        self,
        name: str,
        tracks: list,
        language: str = "eng",
        tmdb_id="",
    ):
        super().__init__("TV Show", name, tracks, language, tmdb_id)

    def make_dict(self, super_dict: Optional[dict] = None, no_tracks: bool = False) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        return DiscType.make_dict(self, super_dict, no_tracks)

    def track_title(self, index: int):
        """generates the title for the track"""
        return f"{self.name.capitalize()} - {self.tracks[index].title}"

    def html_create_data(self, read_only: bool = False) -> dict:
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

        imdbid = ConfigObjString(
            "imdbid",
            "",
            "IMDB ID",
            "Enter the IMDB ID here",
            button=Button("Search By IMDB ID", "tvSearchIMDBid", True, item_width=175),
        )

        tmdbid = ConfigObjString(
            "tmdbid",
            "",
            "TMDB ID",
            "Enter the TMDB ID here",
            button=Button("Search By TMDB ID", "tvSearchTMDBid", True, item_width=175),
        )
        tmdbid.value = self.tmdb_id

        return {
            "search": True,
            "disc_type": self.disc_type,
            "disc_data_items": [
                {
                    "type": "hidden",
                    "var_name": "disc_type",
                    "value": self.disc_type,
                },
                {
                    "type": "hidden",
                    "var_name": "disc_tmdbid",
                    "value": self.tmdb_id,
                },
                {
                    "type": "hidden",
                    "var_name": "disc_name",
                    "value": self.name,
                },
                {
                    "type": "hidden",
                    "var_name": "disc_language",
                    "value": self.language,
                },
            ],
            "disc_items": [
                name.html_dict(""),
                tvdbid.html_dict(""),
                imdbid.html_dict(""),
                tmdbid.html_dict(""),
            ],
        }

    def html_show_data(self, read_only: bool = False) -> dict:
        """returns the data for html"""
        data = Scraper.get_tvshow_details(self.tmdb_id)
        return_dict = {
            "poster_url": Scraper.image_base
            + Scraper.image_config["poster_sizes"][2]
            + data.poster_path,
            "title": data.title,
            "original_title": data.original_title,
            "original_language": data.original_language,
            "release_date": data.release_date,
            "overview": data.overview,
            "tracks": [x.html_create_data(i + 1, read_only) for i, x in enumerate(self.tracks)],
        }

        return return_dict
