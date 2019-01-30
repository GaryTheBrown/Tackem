'''disc type information'''
from abc import ABCMeta, abstractmethod
import datetime
import json
from libs import html_parts
from libs.data.languages import Languages
from . import video_track_type as track_type
TYPES = {"Movie":"film",
         "TV Show":"tv"
        }

class DiscType(metaclass=ABCMeta):
    '''Master Disc Type'''
    def __init__(self, disc_type, name, info, tracks, language):
        if disc_type in TYPES:
            self._disc_type = disc_type
        self._name = name
        self._info = info
        if isinstance(tracks, list):
            self._tracks = tracks
        else:
            self._tracks = []
        if len(language) == 2 and isinstance(language, str):
            self._language = language
        else:
            self._language = "en"

    def disc_type(self):
        '''returns the type'''
        return self._disc_type

    def name(self):
        '''returns the name'''
        return self._name

    def info(self):
        '''returns the temp info'''
        return self._info

    def tracks(self):
        '''returns the tracks'''
        return self._tracks

    def language(self):
        '''returns the discs main language'''
        return self._language

    def set_track(self, track_id, track):
        '''sets the tracks'''
        if self._tracks is not None:
            self._tracks[track_id] = track

    def set_tracks(self, tracks):
        '''sets the tracks'''
        if self._tracks is not None and isinstance(tracks, list):
            self._tracks = tracks

    def make_dict(self, super_dict=None, no_tracks=False):
        '''returns the tracks'''
        if super_dict is None:
            super_dict = {}
        super_dict["disc_type"] = self._disc_type
        super_dict["info"] = self._info
        if not no_tracks:
            track_list = []
            for track in self._tracks:
                if track is None:
                    track_list.append(None)
                else:
                    track_list.append(track.make_dict())
            super_dict["tracks"] = track_list
        return super_dict

    def _change_section_html(self):
        '''change section code'''
        return "<div class=\"onclick topright\" onclick=\"disctype('change');\">(change)</div>"

    @abstractmethod
    def get_edit_panel(self, search=True):
        '''returns the edit panel'''
        pass

    def _get_edit_panel_top(self):
        '''returns the edit panel'''
        html = ""
        html += html_parts.item("info", "Temp Disc Info",
                                "Put some useful info in here for use during renaming",
                                html_parts.input_box("text", "info", self._info),
                                True)
        return html

    def _get_edit_panel_bottom(self, search=True):
        '''returns the edit panel'''
        html = ""
        html += html_parts.item("originallanguage", "Original Language",
                                "Choose the Original Language here",
                                html_parts.select_box("originallanguage", self._language,
                                                      Languages().config_option_2(),
                                                      disabled=search),
                                True)
        return html
class MovieDiscType(DiscType):
    '''Movie Disc Type'''
    def __init__(self, name, info, year, imdbid, tracks, language="eng"):
        super().__init__("Movie", name, info, tracks, language)
        current_year = int(datetime.date.today().year)
        if year == 0:
            self._year = ""
        elif year >= 1888 and year <= current_year:
            self._year = year
        elif year < 1888:
            self._year = 1888
        elif year > current_year:
            self._year = current_year
        self._imdbid = imdbid

    def year(self):
        '''returns movie year'''
        return self._year

    def imdbid(self):
        '''returns movie imdbid'''
        return self._imdbid

    def make_dict(self, super_dict=None, no_tracks=False):
        '''returns the tracks'''
        if super_dict is None:
            super_dict = {}
        super_dict["name"] = self._name
        super_dict["year"] = self._year
        super_dict["imdbid"] = self._imdbid
        return super().make_dict(super_dict, no_tracks)

    def get_edit_panel(self, search=True):
        '''returns the edit panel'''
        html = html_parts.hidden("disc_type", "Movie", True)
        html += super()._get_edit_panel_top()
        html += html_parts.item("name", "Movie Title",
                                "Enter the name of the movie here",
                                html_parts.input_box("text", "name", self._name),
                                True)
        max_year = int(datetime.date.today().year)
        html += html_parts.item("year", "Year",
                                "Enter the year here",
                                html_parts.input_box("number", "year", self._year,
                                                     minimum=1888, maximum=max_year),
                                True)
        if search:
            html += html_parts.item("blank", "",
                                    "Search The Movie Database by Name (And year if known)",
                                    html_parts.input_button("Search By Name",
                                                            "ButtonSearchMovie();"),
                                    True)
        html += html_parts.item("imdbid", "IMDB ID",
                                "Enter the IMDB ID here",
                                html_parts.input_box("text", "imdbid", self._imdbid),
                                True)
        if search:
            html += html_parts.item("blank", "",
                                    "Search The Movie Database by IMDB ID",
                                    html_parts.input_button("Search By IMDB ID",
                                                            "ButtonFindMovie();"),
                                    True)
        html += super()._get_edit_panel_bottom(search)
        return html_parts.panel("Movie Information", self._change_section_html(), "", "",
                                html, True)

class TVShowDiscType(DiscType):
    '''TV Show Disc Type'''
    def __init__(self, name, info, tvdbid, tracks, language="eng"):
        super().__init__("TV Show", name, info, tracks, language)
        self._tvdbid = tvdbid

    def tvdbid(self):
        '''returns TV Show name'''
        return self._tvdbid

    def make_dict(self, super_dict=None, no_tracks=False):
        '''returns the tracks'''
        if super_dict is None:
            super_dict = {}
        super_dict["name"] = self._name
        super_dict["tvdbid"] = self._tvdbid
        return super().make_dict(super_dict, no_tracks)

    def get_edit_panel(self, search=True):
        '''returns the edit panel'''
        html = html_parts.hidden("disc_type", "TV Show", True)
        html += super()._get_edit_panel_top()
        html += html_parts.item("name", "TV Show Name",
                                "Enter the name of the TV Show here",
                                html_parts.input_box("text", "name", self._name),
                                True)
        if search:
            html += html_parts.item("blank", "",
                                    "Search The Movie Database by Name (And year if known)",
                                    html_parts.input_button("Search By Name",
                                                            "ButtonSearchTVShow();"),
                                    True)
        html += html_parts.item("tvdbid", "TVDB ID",
                                "Enter the TVDB ID here",
                                html_parts.input_box("text", "tvdbid", self._tvdbid),
                                True)
        if search:
            html += html_parts.item("blank", "",
                                    "Search The Movie Database by TVDB ID",
                                    html_parts.input_button("Search By TVDB ID",
                                                            "ButtonFindTVShow();"),
                                    True)
        html += super()._get_edit_panel_bottom(search)
        return html_parts.panel("TV Show Information", self._change_section_html(), "", "",
                                html, True)

def make_disc_type(data):
    '''transforms the data returned from the DB or API to the classes above'''
    if isinstance(data, str):
        data = json.loads(data)
    tracks = []
    if 'tracks' in data:
        for track in data['tracks']:
            tracks.append(track_type.make_track_type(track))
    if data['disc_type'].replace(" ", "").lower() == "movie":
        return MovieDiscType(data.get('name', ""), data.get('info', ""), data.get('year', ""),
                             data.get('imdbid', ""), tracks)
    if data['disc_type'].replace(" ", "").lower() == "tvshow":
        return TVShowDiscType(data.get('name', ""), data.get('info', ""),
                              data.get('tvdbid', ""), tracks)
    return None

def make_blank_disc_type(disc_type_code):
    '''make the blank disc type'''
    if disc_type_code.replace(" ", "").lower() == "movie":
        return MovieDiscType("", "", 0, "", None)
    elif disc_type_code.replace(" ", "").lower() == "tvshow":
        return TVShowDiscType("", "", "", None)
    return None
