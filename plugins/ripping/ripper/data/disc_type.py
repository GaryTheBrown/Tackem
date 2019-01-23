'''disc type information'''
from abc import ABCMeta, abstractmethod
import datetime
import json
from libs import html_parts
from .video_track_type import VideoTrackType
from . import video_track_type as track_type
TYPES = {"Movie":"film",
         "TV Show":"tv"
        }

class DiscType(metaclass=ABCMeta):
    '''Master Disc Type'''
    def __init__(self, disc_type, info, tracks, language):
        if disc_type in TYPES:
            self._disc_type = disc_type
        self._info = info
        if isinstance(tracks, list) and all(issubclass(type(x), VideoTrackType) for x in tracks):
            self._tracks = tracks
        if len(language) == 3 and isinstance(language, str):
            self._language = language

    def disc_type(self):
        '''returns the type'''
        return self._disc_type

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
        if no_tracks:
            track_list = []
            for track in self._tracks:
                track_list.append(track.__dict__)
            super_dict["track_list"] = track_list
        return super_dict

    @abstractmethod
    def get_edit_panel(self):
        '''returns the edit panel'''
        pass

class MovieDiscType(DiscType):
    '''Movie Disc Type'''
    def __init__(self, name, info, year, imdb_id, tracks, language="eng"):
        super().__init__("Movie", info, tracks, language)
        self._name = name
        current_year = int(datetime.date.today().year)
        if year >= 1888 and year <= current_year:
            self._year = year
        elif year < 1888:
            self._year = 1888
        elif year > current_year:
            self._year = current_year
        self._imdb_id = imdb_id

    def name(self):
        '''returns movie name'''
        return self._name

    def year(self):
        '''returns movie year'''
        return self._year

    def imdb_id(self):
        '''returns movie imdb_id'''
        return self._imdb_id

    def make_dict(self, super_dict=None, no_tracks=False):
        '''returns the tracks'''
        if super_dict is None:
            super_dict = {}
        super_dict["name"] = self._name
        super_dict["year"] = self._year
        super_dict["imdb_id"] = self._imdb_id
        return super().make_dict(super_dict, no_tracks)

    def get_edit_panel(self):
        '''returns the edit panel'''
        section_html = html_parts.hidden("disc_type", "Movie", True)
        section_html += html_parts.item("name", "Movie Title",
                                        "Enter the name of the movie here",
                                        html_parts.input_box("text", "name", self._name),
                                        True)
        section_html += html_parts.item("info", "Disc Info",
                                        "Put some useful info in here for use during renaming",
                                        html_parts.input_box("text", "info", self._info),
                                        True)
        section_html += html_parts.item("imdbid", "IMDB ID",
                                        "Enter the IMDB ID here",
                                        html_parts.input_box("text", "imdbid", self._imdb_id,
                                                             max_length=8),
                                        True)
        max_year = int(datetime.date.today().year)
        section_html += html_parts.item("year", "Year",
                                        "Enter the year here",
                                        html_parts.input_box("number", "year", self._year,
                                                             minimum=1888, maximum=max_year),
                                        True)
        return html_parts.panel("Movie Information", "", "", "", section_html, True)

class TVShowDiscType(DiscType):
    '''TV Show Disc Type'''
    def __init__(self, name, info, tvdb_id, tracks, language="eng"):
        super().__init__("TV Show", info, tracks, language)
        self._name = name
        self._tvdb_id = tvdb_id

    def name(self):
        '''returns TV Show name'''
        return self._name

    def tvdb_id(self):
        '''returns TV Show name'''
        return self._tvdb_id

    def make_dict(self, super_dict=None, no_tracks=False):
        '''returns the tracks'''
        if super_dict is None:
            super_dict = {}
        super_dict["name"] = self._name
        super_dict["tvdb_id"] = self._tvdb_id
        return super().make_dict(super_dict, no_tracks)

    def get_edit_panel(self):
        '''returns the edit panel'''
        section_html = html_parts.hidden("disc_type", "TV Show", True)
        section_html += html_parts.item("name", "Tv Show Name",
                                        "Enter the name of the TV Show here",
                                        html_parts.input_box("text", "name", self._name),
                                        True)
        section_html += html_parts.item("info", "Disc Info",
                                        "Put some useful info in here for use during renaming",
                                        html_parts.input_box("text", "info", self._info),
                                        True)
        section_html += html_parts.item("tvdbid", "TVDB ID",
                                        "Enter the TVDB ID here",
                                        html_parts.input_box("text", "tvdbid", self._tvdb_id),
                                        True)
        return html_parts.panel("TV Show Information", "", "", "", section_html, True)

def make_disc_type(data):
    '''transforms the data returned from the DB or API to the classes above'''
    if isinstance(data, str):
        data = json.loads(data)
    tracks = []
    for track in data['tracks']:
        track.append(track_type.make_track_type(track))

    if data['disc_type'].lower() == "movie":
        return MovieDiscType(data['name'], data['info'], data['year'], data['imdb_id'], tracks)
    if data['disc_type'].lower() == "tv show":
        return TVShowDiscType(data['name'], data['info'], data['tvdb_id'], tracks)
    return None

def make_blank_disc_type(disc_type_code):
    '''make the blank disc type'''
    if disc_type_code.lower() == "movie":
        return MovieDiscType("", "", 0, "", None)
    elif disc_type_code.lower() == "tv show":
        return TVShowDiscType("", "", "", None)
    return None

def save_html_to_disc_type(data):
    '''transforms the data returned from the DB or API to the classes above'''
    tracks = []
    # for track in data['tracks']:
    #     track.append(track_type.make_track_type(track))

    if data['disc_type'].lower() == "movie":
        return MovieDiscType(data['name'], data['info'], data['year'], data['imdbid'], tracks)
    if data['disc_type'].lower() == "tv show":
        return TVShowDiscType(data['name'], data['info'], data['tvdbid'], tracks)
    return None
