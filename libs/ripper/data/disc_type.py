"""disc type information"""
from abc import ABCMeta, abstractmethod
import datetime
import json
from typing import Optional, Union
from . import video_track_type as track_type

TYPES = {"Movie": "film", "TV Show": "tv", "Documentary": "video", "Other": "question"}


class DiscType(metaclass=ABCMeta):
    """Master Disc Type"""

    def __init__(self, disc_type, name, info, tracks, language, moviedbid):
        self.__disc_type = disc_type if disc_type in TYPES else ""
        self.__name = name
        self.__info = info
        self.__tracks = tracks if isinstance(tracks, list) else []
        self.__language = (
            language if len(language) == 2 and isinstance(language, str) else "en"
        )
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
    def info(self) -> str:
        """returns the temp info"""
        return self.__info

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

    @abstractmethod
    def make_dict(
        self, super_dict: Optional[dict] = None, no_tracks: bool = False
    ) -> dict:
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

    def _change_section_html(self) -> str:
        """change section code"""
        return '<div class="onclick topright" onclick="disctype(\'change\');">(change)</div>'

    # @abstractmethod
    # def get_edit_panel(self, search=True):
    #     '''returns the edit panel'''

    # def _get_edit_panel_top(self):
    #     '''returns the edit panel'''
    #     html = html_parts.hidden("disc_type", self._disc_type, True)
    #     html += html_parts.item("info", "Temp Disc Info",
    #                             "Put some useful info in here for use during renaming",
    #                             html_parts.input_box(
    #                                 "text", "info", self._info),
    #                             True)
    #     return html

    # def _get_edit_panel_bottom(self, search=True):
    #     '''returns the edit panel'''
    #     html = ""
    #     html += html_parts.item("language", "Original Language",
    #                             "Choose the Original Language here",
    #                             html_parts.select_box("language", self._language,
    #                                                   Languages.config_option_2(),
    #                                                   disabled=search),
    #                             True)
    #     return html


class MovieDiscType(DiscType):
    """Movie Disc Type"""

    def __init__(
        self,
        name: str,
        info: str,
        year: int,
        imdbid: str,
        tracks: list,
        language: str = "eng",
        moviedbid: str = "",
    ):
        super().__init__("Movie", name, info, tracks, language, moviedbid)
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

    def make_dict(
        self, super_dict: Optional[dict] = None, no_tracks: bool = False
    ) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["year"] = self.__year
        super_dict["imdbid"] = self.__imdbid
        return super().make_dict(super_dict, no_tracks)

    # def get_edit_panel(self, search=True):
    #     '''returns the edit panel'''
    #     html = html_parts.hidden("moviedbid", self._moviedbid, True)
    #     html += super()._get_edit_panel_top()
    #     html += html_parts.item("name", "Movie Title",
    #                             "Enter the name of the movie here",
    #                             html_parts.input_box(
    #                                 "text", "name", self._name),
    #                             True)
    #     max_year = int(datetime.date.today().year)
    #     html += html_parts.item("year", "Year",
    #                             "Enter the year here",
    #                             html_parts.input_box("number", "year", self._year,
    #                                                  minimum=1888, maximum=max_year),
    #                             True)
    #     if search:
    #         html += html_parts.item("blank", "",
    #                                 "Search The Movie Database by Name (And year if known)",
    #                                 html_parts.input_button("Search By Name",
    #                                                         "ButtonSearchMovie();"),
    #                                 True)
    #     html += html_parts.item("imdbid", "IMDB ID",
    #                             "Enter the IMDB ID here",
    #                             html_parts.input_box(
    #                                 "text", "imdbid", self._imdbid),
    #                             True)
    #     if search:
    #         html += html_parts.item("blank", "",
    #                                 "Search The Movie Database by IMDB ID",
    #                                 html_parts.input_button("Search By IMDB ID",
    #                                                         "ButtonFindMovie();"),
    #                                 True)
    #     html += super()._get_edit_panel_bottom(search)
    #     return html_parts.panel("Movie Information", self._change_section_html(), "", "",
    #                             html, True)


class TVShowDiscType(DiscType):
    """TV Show Disc Type"""

    def __init__(
        self,
        name: str,
        info: str,
        tvdbid: str,
        tracks: list,
        language: str = "eng",
        moviedbid="",
    ):
        super().__init__("TV Show", name, info, tracks, language, moviedbid)
        self.__tvdbid = tvdbid

    @property
    def tvdbid(self) -> str:
        """returns TV Show name"""
        return self.__tvdbid

    def make_dict(
        self, super_dict: Optional[dict] = None, no_tracks: bool = False
    ) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["tvdbid"] = self.__tvdbid
        return super().make_dict(super_dict, no_tracks)

    # def get_edit_panel(self, search=True):
    #     '''returns the edit panel'''
    #     html = html_parts.hidden("moviedbid", self._moviedbid, True)
    #     html += super()._get_edit_panel_top()
    #     html += html_parts.item("name", "TV Show Name",
    #                             "Enter the name of the TV Show here",
    #                             html_parts.input_box(
    #                                 "text", "name", self._name),
    #                             True)
    #     if search:
    #         html += html_parts.item("blank", "",
    #                                 "Search The Movie Database by Name (And year if known)",
    #                                 html_parts.input_button("Search By Name",
    #                                                         "ButtonSearchTVShow();"),
    #                                 True)
    #     html += html_parts.item("tvdbid", "TVDB ID",
    #                             "Enter the TVDB ID here",
    #                             html_parts.input_box(
    #                                 "text", "tvdbid", self._tvdbid),
    #                             True)
    #     if search:
    #         html += html_parts.item("blank", "",
    #                                 "Search The Movie Database by TVDB ID",
    #                                 html_parts.input_button("Search By TVDB ID",
    #                                                         "ButtonFindTVShow();"),
    #                                 True)
    #     html += super()._get_edit_panel_bottom(search)
    #     return html_parts.panel("TV Show Information", self._change_section_html(), "", "",
    #                             html, True)


class DocumentaryDiscType(DiscType):
    """TV Show Disc Type"""

    def __init__(self, name: str, info: str, tracks: list, language: str = "eng"):
        super().__init__("Documentary", name, info, tracks, language, None)

    def make_dict(
        self, super_dict: Optional[dict] = None, no_tracks: bool = False
    ) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        return super().make_dict(super_dict, no_tracks)

    # def get_edit_panel(self, search=True):
    #     '''returns the edit panel'''
    #     html = super()._get_edit_panel_top()
    #     html += html_parts.item("name", "Documentary Name",
    #                             "Enter the name of the Documentary here",
    #                             html_parts.input_box(
    #                                 "text", "name", self._name),
    #                             True)
    #     html += super()._get_edit_panel_bottom(False)
    #     html += html_parts.text_item("*Please Choose Other For All Tracks")
    #     return html_parts.panel("Documentary Information", self._change_section_html(), "", "",
    #                             html, True)


class OtherDiscType(DiscType):
    """TV Show Disc Type"""

    def __init__(self, name: str, info: str, tracks: list, language: str = "eng"):
        super().__init__("Other", name, info, tracks, language, None)

    def make_dict(
        self, super_dict: Optional[dict] = None, no_tracks: bool = False
    ) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        return super().make_dict(super_dict, no_tracks)

    # def get_edit_panel(self, search=True):
    #     '''returns the edit panel'''
    #     html = super()._get_edit_panel_top()
    #     html += html_parts.item("name", "Disc Name",
    #                             "Enter the name of the Disc here",
    #                             html_parts.input_box(
    #                                 "text", "name", self._name),
    #                             True)
    #     html += super()._get_edit_panel_bottom(False)
    #     html += html_parts.text_item("*Please Choose Other For All Tracks")
    #     return html_parts.panel("Disc Information", self._change_section_html(), "", "",
    #                             html, True)


def make_disc_type(data: Union[str, dict]) -> DiscType:
    """transforms the data returned from the DB or API to the classes above"""
    if isinstance(data, str):
        data = json.loads(data)
    tracks = []
    if "tracks" in data:
        for track in data["tracks"]:
            tracks.append(track_type.make_track_type(track))
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
        return MovieDiscType("", "", 0, "", None, "en", "")
    if disc_type_code.replace(" ", "").lower() == "tvshow":
        return TVShowDiscType("", "", "", None, "en", "")
    if disc_type_code.replace(" ", "").lower() == "documentary":
        return DocumentaryDiscType("", "", None, "en")
    if disc_type_code.replace(" ", "").lower() == "other":
        return OtherDiscType("", "", None, "en")
    return None
