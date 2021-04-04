"""disc type information"""
import datetime
import json
from abc import ABCMeta
from abc import abstractmethod
from typing import Dict
from typing import Optional
from typing import Union

from data.video_track_type import make_track_type
from libs.classproperty import classproperty
from libs.config.obj.data.button import Button
from libs.config.obj.string import ConfigObjString


class DiscType(metaclass=ABCMeta):
    """Master Disc Type"""

    @classproperty
    def TYPESANDICONS(cls) -> Dict[str, str]:
        """returns a list of types with Font Awsome Free Icons"""
        # Do we want to add and allow an adult section?
        return {
            "Movie": "film",
            "TV Show": "tv",
            "Documentary": "info-circle",
            "Home Movie": "users",
            "Music Video": "music",
            "Other": "question",
        }

    def __init__(self, disc_type: str, name: str, tracks: list, language: str, moviedbid: str):
        self.__disc_type = disc_type if disc_type in self.TYPESANDICONS else ""
        self.__name = name
        self.__tracks = tracks if isinstance(tracks, list) else []
        self.__language = language if len(language) == 2 and isinstance(language, str) else "en"
        self.__moviedbid = moviedbid

    @property
    def disc_type(self) -> str:
        """returns the type"""
        return self.__disc_type

    @property
    def name(self) -> str:
        """returns the name"""
        return self.__name

    @property
    def tracks(self) -> list:
        """returns the tracks"""
        return self.__tracks

    @property
    def language(self) -> str:
        """returns the discs main language"""
        return self.__language

    @property
    def moviedbid(self) -> str:
        """returns the moviedbid"""
        return self.__moviedbid

    def set_track(self, track_id, track):
        """sets the tracks"""
        if self.__tracks is not None:
            self.__tracks[track_id] = track

    def set_tracks(self, tracks) -> Optional[list]:
        """sets the tracks"""
        if self.__tracks is not None and isinstance(tracks, list):
            self.__tracks = tracks

    def json(self) -> str:
        """returns the Disc Type as a Json String"""
        return json.dumps(self.make_dict())

    def make_dict(self, super_dict: Optional[dict] = None, no_tracks: bool = False) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["disc_type"] = self.__disc_type
        super_dict["name"] = self.__name
        super_dict["info"] = self.__info
        super_dict["language"] = self.__language
        super_dict["moviedbid"] = self.__moviedbid
        if not no_tracks:
            track_list = []
            for track in self.__tracks:
                if track is None:
                    track_list.append(None)
                else:
                    track_list.append(track.make_dict())
            super_dict["tracks"] = track_list
        return super_dict

    @abstractmethod
    def track_title(self, index: int):
        """generates the title for the track"""

    @abstractmethod
    def html_data(self) -> dict:
        """returns the data for html"""


class MovieDiscType(DiscType):
    """Movie Disc Type"""

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

    def html_data(self) -> dict:
        """returns the data for html"""
        name = ConfigObjString(
            "name",
            "",
            "Movie Title",
            "Enter the name of the movie here",
            button=Button("Find By Title", "movieSearch", True),
        )
        name.value = self.name

        imdbid = ConfigObjString(
            "imbbid",
            "",
            "IMDB ID",
            "Enter the IMDB ID here",
            button=Button("Find By IMDB ID", "movieSearchIMDBid", True),
        )
        imdbid.value = self.imdbid

        tmdbid = ConfigObjString(
            "tmbbid",
            "",
            "TMDB ID",
            "Enter the TMDB ID here",
            button=Button("Find By TMDB ID", "movieSearchTMDBid", True),
        )
        tmdbid.value = self.moviedbid

        return {
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": "disc_type",
                    "value": self.disc_type,
                },
                name.html_dict(""),
                imdbid.html_dict(""),
                tmdbid.html_dict(""),
            ]
        }


class TVShowDiscType(DiscType):
    """TV Show Disc Type"""

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

    def html_data(self) -> dict:
        """returns the data for html"""
        name = ConfigObjString(
            "name",
            "",
            "TV Show Name",
            "Enter the name of the TV Show here",
            button=Button("Find By Title", "tvSearch", True),
        )
        name.value = self.name

        tvdbid = ConfigObjString(
            "tvdbid",
            "",
            "TVDB ID",
            "Enter the TVDB ID here",
            button=Button("Find By TVDB ID", "tvSearchTVDBid", True),
        )
        tvdbid.value = self.tvdbid

        tmdbid = ConfigObjString(
            "tmbbid",
            "",
            "TMDB ID",
            "Enter the TMDB ID here",
            button=Button("Find By TMDB ID", "tvSearchTMDBid", True),
        )
        tmdbid.value = self.moviedbid

        return {
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": "disc_type",
                    "value": self.disc_type,
                },
                name.html_dict(""),
                tvdbid.html_dict(""),
                tmdbid.html_dict(""),
            ]
        }


class DocumentaryDiscType(DiscType):
    """Documentary Disc Type"""

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

    def html_data(self) -> dict:
        """returns the data for html"""
        name = ConfigObjString(
            "name",
            "",
            "Documentary Name",
            "Enter the name of the Documentary here",
            button=Button("Find By Title", "docSearch", True),
        )
        name.value = self.name

        imdbid = ConfigObjString(
            "imbbid",
            "",
            "IMDB ID",
            "Enter the IMDB ID here",
            button=Button("Find By IMDB ID", "docSearchIMDBid", True),
        )
        imdbid.value = self.imdbid

        tvdbid = ConfigObjString(
            "tvdbid",
            "",
            "TVDB ID",
            "Enter the TVDB ID here",
            button=Button("Find By TVDB ID", "docSearchTVDBid", True),
        )
        tvdbid.value = self.tvdbid

        tmdbid = ConfigObjString(
            "tmbbid",
            "",
            "TMDB ID",
            "Enter the TMDB ID here",
            button=Button("Find By TMDB ID", "docSearchTMDBid", True),
        )
        tmdbid.value = self.moviedbid

        return {
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
            ]
        }


class OtherDiscType(DiscType):
    """Other Disc Type"""

    def __init__(self, name: str, info: str, tracks: list, language: str = "eng"):
        super().__init__("Other", name, tracks, language, None)
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
        return f"{self.name.capitalize()} - {self.tracks[index].title}"

    def html_data(self) -> dict:
        """returns the data for html"""
        name = ConfigObjString(
            "name",
            "",
            "Disc Name",
            "Enter the name of the Disc here",
        )
        name.value = self.name

        return {
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": "disc_type",
                    "value": self.disc_type,
                },
                name.html_dict(""),
            ]
        }


class MusicVideoDiscType(DiscType):
    """Private Disc Type"""

    def __init__(self, name: str, info: str, tracks: list, language: str = "eng"):
        super().__init__("Private", name, tracks, language, None)
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
        return f"PRIVATE {self.name.capitalize()} - {self.tracks[index].title}"

    def html_data(self) -> dict:
        """returns the data for html"""
        name = ConfigObjString(
            "name",
            "",
            "Disc Name",
            "Enter the name of the Disc here",
        )
        name.value = self.name

        return {
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": "disc_type",
                    "value": self.disc_type,
                },
                name.html_dict(""),
            ]
        }


class HomeMovieDiscType(DiscType):
    """HomeMovie Disc Type"""

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

    def html_data(self) -> dict:
        """returns the data for html"""
        name = ConfigObjString(
            "name",
            "",
            "Disc Name",
            "Enter the name of the Disc here",
        )
        name.value = self.name

        return {
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": "disc_type",
                    "value": self.disc_type,
                },
                name.html_dict(""),
            ]
        }


def make_disc_type(data: Union[str, dict]) -> DiscType:
    """transforms the data returned from the DB or API to the classes above"""
    if isinstance(data, str):
        data = json.loads(data)
    tracks = []
    if "tracks" in data:
        for track in data["tracks"]:
            tracks.append(make_track_type(track))
    if data["disc_type"].replace(" ", "").lower() == "movie":
        return MovieDiscType(
            data.get("name", ""),
            data.get("info", ""),
            data.get("year", ""),
            data.get("imdbid", ""),
            tracks,
            data.get("language", "en"),
            data.get("moviedbid", ""),
        )
    if data["disc_type"].replace(" ", "").lower() == "tvshow":
        return TVShowDiscType(
            data.get("name", ""),
            data.get("info", ""),
            data.get("tvdbid", ""),
            tracks,
            data.get("language", "en"),
            data.get("moviedbid", ""),
        )
    if data["disc_type"].replace(" ", "").lower() == "documentary":
        return DocumentaryDiscType(
            data.get("name", ""),
            data.get("info", ""),
            tracks,
            data.get("language", "en"),
        )
    if data["disc_type"].replace(" ", "").lower() == "musicvideo":
        return MusicVideoDiscType(
            data.get("name", ""),
            data.get("info", ""),
            tracks,
            data.get("language", "en"),
        )
    if data["disc_type"].replace(" ", "").lower() == "homemovie":
        return HomeMovieDiscType(
            data.get("name", ""),
            data.get("info", ""),
            tracks,
            data.get("language", "en"),
        )
    if data["disc_type"].replace(" ", "").lower() == "other":
        return OtherDiscType(
            data.get("name", ""),
            data.get("info", ""),
            tracks,
            data.get("language", "en"),
        )
    return None


def make_blank_disc_type(disc_type_code: str) -> DiscType:
    """make the blank disc type"""
    if disc_type_code.replace(" ", "").lower() == "movie":
        return MovieDiscType("", 0, "", None, "en", "")
    if disc_type_code.replace(" ", "").lower() == "tvshow":
        return TVShowDiscType("", "", None, "en", "")
    if disc_type_code.replace(" ", "").lower() == "documentary":
        return DocumentaryDiscType("", None, "en")
    if disc_type_code.replace(" ", "").lower() == "musicvideo":
        return MusicVideoDiscType("", "", None, "en")
    if disc_type_code.replace(" ", "").lower() == "homemovie":
        return HomeMovieDiscType("", "", None, "en")
    if disc_type_code.replace(" ", "").lower() == "other":
        return OtherDiscType("", "", None, "en")
    return None
