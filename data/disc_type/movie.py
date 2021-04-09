"""disc type information"""
import datetime
from typing import List
from typing import Optional

from data.disc_type.base import DiscType
from libs.config.obj.data.button import Button
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.integer_number import ConfigObjIntegerNumber
from libs.config.obj.string import ConfigObjString


class MovieDiscType(DiscType):
    """Movie Disc Type"""

    _track_types: List[str] = ["dontrip", "feature", "trailer", "extra"]

    def __init__(
        self,
        name: str,
        year: int,
        imdbid: str,
        tracks: list,
        language: str = "eng",
        moviedbid: str = "",
    ):
        super().__init__("Movie", name, tracks, language, moviedbid)
        current_year = int(datetime.date.today().year)
        if year == 0:
            self.__year = ""
        elif int(year) >= 1888 and int(year) <= current_year:
            self.__year = int(year)
        elif year < 1888:
            self.__year = 1888
        elif year > current_year:
            self.__year = current_year
        self.__imdbid = imdbid

    @property
    def year(self) -> int:
        """returns movie year"""
        return self.__year

    @property
    def imdbid(self) -> str:
        """returns movie imdbid"""
        return self.__imdbid

    def make_dict(self, super_dict: Optional[dict] = None, no_tracks: bool = False) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["year"] = self.__year
        super_dict["imdbid"] = self.__imdbid
        return DiscType.make_dict(self, super_dict, no_tracks)

    def track_title(self, index: int):
        """generates the title for the track"""
        return f"{self.name.capitalize()} ({self.year}) - {self.tracks[index].title}"

    def html_search_data(self) -> dict:
        """returns the data for html"""
        name = ConfigObjString(
            "name",
            "",
            "Movie Title",
            "Enter the name of the movie here",
            button=Button("Search By Title", "movieSearch", True, item_width=175),
        )
        name.value = self.name

        year = ConfigObjIntegerNumber(
            "year",
            0,
            "Year",
            "Enter the year here to help the search by title",
            input_attributes=InputAttributes(min=1888, max=int(datetime.date.today().year)),
        )
        year.value = self.year

        imdbid = ConfigObjString(
            "imbbid",
            "",
            "IMDB ID",
            "Enter the IMDB ID here",
            button=Button("Search By IMDB ID", "movieSearchIMDBid", True, item_width=175),
        )
        imdbid.value = self.imdbid

        tmdbid = ConfigObjString(
            "tmbbid",
            "",
            "TMDB ID",
            "Enter the TMDB ID here",
            button=Button("Search By TMDB ID", "movieSearchTMDBid", True, item_width=175),
        )
        tmdbid.value = self.moviedbid

        year_html = year.html_dict("")
        year_html["value"] = ""
        return {
            "no_search": False,
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": "disc_type",
                    "value": self.disc_type,
                },
                name.html_dict(""),
                year_html,
                imdbid.html_dict(""),
                tmdbid.html_dict(""),
            ],
        }
