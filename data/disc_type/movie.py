"""disc type information"""
import datetime
from typing import List
from typing import Optional

from config.backend.obj.data.button import Button
from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.obj.integer_number import ConfigObjIntegerNumber
from config.backend.obj.string import ConfigObjString
from data.disc_type.base import DiscType
from libs.scraper import Scraper


class MovieDiscType(DiscType):
    """Movie Disc Type"""

    _track_types: List[str] = ["Dont Rip", "Feature", "Trailer", "Extra"]

    def __init__(
        self,
        name: str,
        year: int,
        tracks: list,
        language: str = "eng",
        tmdb_id: int = 0,
    ):
        super().__init__("Movie", name, tracks, language, tmdb_id)
        current_year = int(datetime.date.today().year)
        if year == 0:
            self.__year = ""
        elif int(year) >= 1888 and int(year) <= current_year:
            self.__year = int(year)
        elif year < 1888:
            self.__year = 1888
        elif year > current_year:
            self.__year = current_year

    @property
    def year(self) -> int:
        """returns movie year"""
        return self.__year

    def make_dict(self, super_dict: Optional[dict] = None, no_tracks: bool = False) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["year"] = self.__year
        return DiscType.make_dict(self, super_dict, no_tracks)

    def track_title(self, index: int):
        """generates the title for the track"""
        return f"{self.name.capitalize()} ({self.year}) - {self.tracks[index].title}"

    def html_create_data(self, read_only: bool = False) -> dict:
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
            "imdbid",
            "",
            "IMDB ID",
            "Enter the IMDB ID here",
            button=Button("Search By IMDB ID", "movieSearchIMDBid", True, item_width=175),
        )

        tmdbid = ConfigObjString(
            "tmdbid",
            "",
            "TMDB ID",
            "Enter the TMDB ID here",
            button=Button("Search By TMDB ID", "movieSearchTMDBid", True, item_width=175),
        )
        tmdbid.value = self.tmdb_id

        year_html = year.html_dict("")
        year_html["value"] = ""
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
                    "var_name": "disc_year",
                    "value": self.year,
                },
                {
                    "type": "hidden",
                    "var_name": "disc_language",
                    "value": self.language,
                },
            ],
            "disc_items": [
                name.html_dict(""),
                year_html,
                imdbid.html_dict(""),
                tmdbid.html_dict(""),
            ],
        }

    def html_show_data(self, read_only: bool = False) -> dict:
        """returns the data for html"""
        data = Scraper.get_movie_details(self.tmdb_id)
        return_dict = {
            "poster_url": Scraper.image_base
            + Scraper.image_config["poster_sizes"][2]
            + data["poster_path"],
            "title": data["title"],
            "original_title": data["original_title"],
            "original_language": data["original_language"],
            "release_date": data["release_date"],
            "overview": data["overview"],
            "tracks": [x.html_create_data(i + 1, read_only) for i, x in enumerate(self.tracks)],
        }

        return return_dict
