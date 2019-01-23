'''video track type information'''
from abc import ABCMeta, abstractmethod
import json
from libs import html_parts
from .stream_type import StreamType

TYPES = {"dontrip":"ban",
         "movie":"film",
         "tvshow":"tv",
         "trailer":"film",
         "extra":"plus",
         "other":"plus"
        }

class VideoTrackType(metaclass=ABCMeta):
    '''Master Type'''
    def __init__(self, video_type, streams):
        if video_type in TYPES:
            self._video_type = video_type
        if isinstance(streams, list) and all(issubclass(type(x), StreamType) for x in streams):
            self._streams = streams

    def video_type(self):
        '''returns the type'''
        return self._video_type

    @abstractmethod
    def get_edit_panel(self):
        '''returns the edit panel'''
        pass

class DONTRIPTrackType(VideoTrackType):
    '''Other Types'''
    def __init__(self, reason):
        super().__init__("dontrip", None)
        self._reason = reason

    def reason(self):
        '''return the reason not to rip this track'''
        return self._reason

    def get_edit_panel(self):
        '''returns the edit panel'''
        section_html = html_parts.hidden("track_%%TRACKINDEX%%_type", "dontrip", True)
        section_html += html_parts.item("track_%%TRACKINDEX%%_reason", "Reason",
                                        "Enter the reason not to rip here",
                                        html_parts.input_box("text",
                                                             "track_%%TRACKINDEX%%_reason",
                                                             self._reason),
                                        True)
        return section_html

class MovieTrackType(VideoTrackType):
    '''Movie Type'''
    def __init__(self, streams=None): # tvshow_link=None, tvshow_special_number=None,
        super().__init__("movie", streams)
    #     self._tvshow_link = tvshow_link
    #     self._tvshow_special_number = tvshow_special_number

    # def tvshow_link(self):
    #     '''return the tv show name for linking'''
    #     return self._tvshow_link

    # def tvshow_special_number(self):
    #     '''return the tv show special number'''
    #     return self._tvshow_special_number

    def get_edit_panel(self):
        '''returns the edit panel'''
        section_html = html_parts.hidden("track_%%TRACKINDEX%%_type", "movie", True)
        return section_html

class TVShowTrackType(VideoTrackType):
    '''TV Show Type'''
    def __init__(self, season_number, episode_number, streams=None):
        super().__init__("tvshow", streams)
        self._season_number = season_number
        self._episode_number = episode_number

    def season_number(self):
        '''returns tv show season number'''
        return self._season_number

    def episode_number(self):
        '''returns tv show episode number'''
        return self._episode_number

    def get_edit_panel(self):
        '''returns the edit panel'''
        section_html = html_parts.hidden("track_%%TRACKINDEX%%_type", "tvshow", True)
        section_html += html_parts.item("track_%%TRACKINDEX%%_season", "Season Number",
                                        "Enter the Season Number here",
                                        html_parts.input_box("number",
                                                             "track_%%TRACKINDEX%%_season",
                                                             self._season_number, minimum=0),
                                        True)
        section_html += html_parts.item("track_%%TRACKINDEX%%_episode", "Episode Number",
                                        "Enter the Episode Number here",
                                        html_parts.input_box("number",
                                                             "track_%%TRACKINDEX%%_episode",
                                                             self._episode_number, minimum=0),
                                        True)
        return section_html

class ExtraTrackType(VideoTrackType):
    '''Extra Type'''
    def __init__(self, name, streams=None):
        super().__init__("extra", streams)
        self._name = name

    def name(self):
        '''returns extra name'''
        return self._name

    # def tvshow_link(self):
    #     '''return the tv show name for linking'''
    #     return self._tvshow_link

    # def tvshow_special_number(self):
    #     '''return the tv show special number'''
    #     return self._tvshow_special_number

    def get_edit_panel(self):
        '''returns the edit panel'''
        section_html = html_parts.hidden("track_%%TRACKINDEX%%_type", "extra", True)
        section_html += html_parts.item("track_%%TRACKINDEX%%_name", "Name",
                                        "Enter the extra name",
                                        html_parts.input_box("text",
                                                             "track_%%TRACKINDEX%%_name",
                                                             self._name),
                                        True)
        return section_html

class TrailerTrackType(VideoTrackType):
    '''trailer Type'''
    def __init__(self, info, streams=None):
        super().__init__("trailer", streams)
        self._info = info

    def info(self):
        '''returns trailers movie info'''
        return self._info

    def get_edit_panel(self):
        '''returns the edit panel'''
        section_html = html_parts.hidden("track_%%TRACKINDEX%%_type", "trailer", True)
        section_html += html_parts.item("track_%%TRACKINDEX%%_info", "Information",
                                        "Enter trailer information here",
                                        html_parts.input_box("text",
                                                             "track_%%TRACKINDEX%%_info",
                                                             self._info),
                                        True)
        return section_html

class OtherTrackType(VideoTrackType):
    '''Other Types'''
    def __init__(self, other_type, streams=None):
        super().__init__("other", streams)
        self._other_type = other_type

    def other_type(self):
        '''returns other type'''
        return self._other_type

    def get_edit_panel(self):
        '''returns the edit panel'''
        section_html = html_parts.hidden("track_%%TRACKINDEX%%_type", "other", True)
        section_html += html_parts.item("track_%%TRACKINDEX%%_othertype", "Other Type",
                                        "What is it?",
                                        html_parts.input_box("text",
                                                             "track_%%TRACKINDEX%%_othertype",
                                                             self._other_type),
                                        True)
        return section_html

def make_track_type(track):
    '''transforms the track returned from the DB or API to the classes above'''
    if isinstance(track, str):
        track = json.loads(track)
        if track is None:
            return None
        elif track['video_type'] == "dontrip":
            return DONTRIPTrackType(track['reason'])
        elif track['video_type'] == "movie":
            return MovieTrackType()
        elif track['video_type'] == "tvshow":
            return TVShowTrackType(track['season_number'], track['episode_number'])
        elif track['video_type'] == "trailer":
            return TrailerTrackType(track['info'])
        elif track['video_type'] == "extra":
            return ExtraTrackType(track['name'])
        elif track['video_type'] == "other":
            return OtherTrackType(track['other_type'])
    return None

def make_blank_track_type(track_type_code):
    '''make the blank track type'''
    if track_type_code.lower() == "dontrip":
        return DONTRIPTrackType("")
    elif track_type_code.lower() == "movie":
        return MovieTrackType()
    elif track_type_code.lower() == "tvshow":
        return TVShowTrackType("", "",)
    elif track_type_code.lower() == "trailer":
        return TrailerTrackType("")
    elif track_type_code.lower() == "extra":
        return ExtraTrackType("")
    elif track_type_code.lower() == "other":
        return OtherTrackType("")
    return None
