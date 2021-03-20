"""video track type information"""
import json
from abc import ABCMeta
from typing import Optional
from typing import Union

from . import stream_type

TYPES = {
    "dontrip": "ban",
    "movie": "film",
    "tvshow": "tv",
    "trailer": "film",
    "extra": "plus",
    "other": "plus",
}


class VideoTrackType(metaclass=ABCMeta):
    """Master Type"""

    def __init__(self, video_type: str, streams: Optional[list], hdr: bool):
        self.__video_type = video_type if video_type in TYPES else ""
        self.__streams = streams if isinstance(streams, list) else []
        self.__hdr = hdr

    @property
    def hdr(self) -> bool:
        """return hdr"""
        return self.__hdr

    @property
    def video_type(self) -> str:
        """returns the type"""
        return self.__video_type

    @property
    def streams(self) -> list:
        """returns streams"""
        return self.__streams

    def _title_html(self, title: str) -> str:
        """title line for sections"""
        return '<h1 class="text-center">' + title + "</h1>"

    def json(self) -> str:
        """returns the Disc Type as a Json String"""
        return json.dumps(self.make_dict())

    def make_dict(self, super_dict: Optional[dict] = None, include_streams: bool = True) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["video_type"] = self.__video_type
        stream_list = []
        if include_streams:
            for stream in self.__streams:
                if stream is None:
                    stream_list.append(None)
                else:
                    stream_list.append(stream.make_dict())
            super_dict["streams"] = stream_list
        super_dict["hdr"] = self.__hdr
        return super_dict

    def _change_section_html(self, track: str) -> str:
        """change section code"""
        html = '<div class="onclick topright" onclick="tracktype(' + str(track)
        html += ", 'change');\">(change)</div>"
        return html

    # def _make_stream_sections(self, ffprobe):
    #     '''creates the stream sections'''
    #     html = ""
    #     for stream_index, stream_type_code in enumerate(ffprobe.get_streams_and_types()):
    #         stream_data = ffprobe.get_stream(stream_index)
    #         if self._streams:
    #             html += self._streams[stream_index].get_edit_panel(stream_data)
    #         else:
    #             temp_stream = stream_type.make_blank_stream_type(
    #                 stream_index, stream_type_code)
    #             html += temp_stream.get_edit_panel(stream_data)
    #     return html_parts.video_panel("Streams", "", html)

    # @abstractmethod
    # def get_edit_panel(self, ffprobe=None):
    #     '''returns the edit panel'''

    # def _get_edit_panel_bottom(self):
    #     '''returns the edit panel'''
    #     html = ""
    #     html += ghtml_parts.item("track_%%TRACKINDEX%%_hdr", "HDR",
    #                              "Is the Track HDR?",
    #                              ghtml_parts.checkbox_single("",
    #                                                          "track_%%TRACKINDEX%%_hdr",
    #                                                          self._hdr),
    #                              True)
    #     return html


class DONTRIPTrackType(VideoTrackType):
    """Other Types"""

    def __init__(self, reason: str):
        super().__init__("dontrip", None, False)
        self.__reason = reason

    @property
    def reason(self) -> str:
        """return the reason not to rip this track"""
        return self.__reason

    def make_dict(self, super_dict: Optional[dict] = None, include_streams: bool = True) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["reason"] = self.__reason
        return super().make_dict(super_dict, include_streams)

    # def get_edit_panel(self, ffprobe=None):
    #     '''returns the edit panel'''
    #     section_html = self._title_html("Don't Rip")
    #     section_html += " " + self._change_section_html("%%TRACKINDEX%%")
    #     section_html += ghtml_parts.hidden(
    #         "track_%%TRACKINDEX%%_video_type", "dontrip", True)
    #     section_html += ghtml_parts.item("track_%%TRACKINDEX%%_reason", "Reason",
    #                                      "Enter the reason not to rip here",
    #                                      ghtml_parts.input_box("text",
    #                                                            "track_%%TRACKINDEX%%_reason",
    #                                                            self._reason),
    #                                      True)
    #     return section_html


class MovieTrackType(VideoTrackType):
    """Movie Type"""

    def __init__(
        self,
        streams: Optional[list] = None,
        tvshow_link=None,
        tvshow_special_number=None,
        hdr: bool = False,
    ):
        super().__init__("movie", streams, hdr)

        self.__tvshow_link = tvshow_link
        self.__tvshow_special_number = tvshow_special_number

    @property
    def tvshow_link(self):
        """return the tv show name for linking"""
        return self.__tvshow_link

    @property
    def tvshow_special_number(self):
        """return the tv show special number"""
        return self.__tvshow_special_number

    def make_dict(self, super_dict: Optional[dict] = None, include_streams: bool = True):
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        if self.__tvshow_link is not None:
            super_dict["tv_show_link"] = self.__tvshow_link
            super_dict["tv_show_special_number"] = self.__tvshow_special_number
        return super().make_dict(super_dict, include_streams)

    # def get_edit_panel(self, ffprobe=None):
    #     '''returns the edit panel'''
    #     section_html = self._title_html("Movie")
    #     section_html += " " + self._change_section_html("%%TRACKINDEX%%")
    #     section_html += ghtml_parts.hidden(
    #         "track_%%TRACKINDEX%%_video_type", "movie", True)
    #     section_html += super()._get_edit_panel_bottom()
    #     if ffprobe:
    #         section_html += self._make_stream_sections(ffprobe)
    #     return section_html


class TVShowTrackType(VideoTrackType):
    """TV Show Type"""

    def __init__(
        self,
        season: int,
        episode: int,
        streams: Optional[list] = None,
        hdr: bool = False,
    ):
        super().__init__("tvshow", streams, hdr)
        self.__season = season
        self.__episode = episode

    @property
    def season(self) -> int:
        """returns tv show season number"""
        return self.__season

    @property
    def episode(self) -> int:
        """returns tv show episode number"""
        return self.__episode

    def make_dict(self, super_dict: Optional[dict] = None, include_streams: bool = True) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["season"] = self.__season
        super_dict["episode"] = self.__episode
        return super().make_dict(super_dict, include_streams)

    # def get_edit_panel(self, ffprobe=None):
    #     '''returns the edit panel'''
    #     section_html = self._title_html("TV Show Episode")
    #     section_html += " " + self._change_section_html("%%TRACKINDEX%%")
    #     section_html += ghtml_parts.hidden(
    #         "track_%%TRACKINDEX%%_video_type", "tvshow", True)
    #     section_html += ghtml_parts.item("track_%%TRACKINDEX%%_season", "Season Number",
    #                                      "Enter the Season Number here",
    #                                      ghtml_parts.input_box("number",
    #                                                            "track_%%TRACKINDEX%%_season",
    #                                                            self._season, minimum=0),
    #                                      True)
    #     section_html += ghtml_parts.item("track_%%TRACKINDEX%%_episode", "Episode Number",
    #                                      "Enter the Episode Number here",
    #                                      ghtml_parts.input_box("number",
    #                                                            "track_%%TRACKINDEX%%_episode",
    #                                                            self._episode, minimum=0),
    #                                      True)
    #     section_html += super()._get_edit_panel_bottom()
    #     if ffprobe:
    #         section_html += self._make_stream_sections(ffprobe)
    #     return section_html


class ExtraTrackType(VideoTrackType):
    """Extra Type"""

    def __init__(self, name: str, streams: Optional[list] = None, hdr: bool = False):
        super().__init__("extra", streams, hdr)
        self.__name = name

    @property
    def name(self) -> str:
        """returns extra name"""
        return self.__name

    def make_dict(self, super_dict: Optional[dict] = None, include_streams: bool = True) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["name"] = self.__name
        return super().make_dict(super_dict, include_streams)

    # def tvshow_link(self):
    #     '''return the tv show name for linking'''
    #     return self._tvshow_link

    # def tvshow_special_number(self):
    #     '''return the tv show special number'''
    #     return self._tvshow_special_number

    # def get_edit_panel(self, ffprobe=None):
    #     '''returns the edit panel'''
    #     section_html = self._title_html("Extra")
    #     section_html += " " + self._change_section_html("%%TRACKINDEX%%")
    #     section_html += ghtml_parts.hidden(
    #         "track_%%TRACKINDEX%%_video_type", "extra", True)
    #     section_html += ghtml_parts.item("track_%%TRACKINDEX%%_name", "Name",
    #                                      "Enter the extra name",
    #                                      ghtml_parts.input_box("text",
    #                                                            "track_%%TRACKINDEX%%_name",
    #                                                            self._name),
    #                                      True)
    #     section_html += super()._get_edit_panel_bottom()
    #     if ffprobe:
    #         section_html += self._make_stream_sections(ffprobe)
    #     return section_html


class TrailerTrackType(VideoTrackType):
    """trailer Type"""

    def __init__(self, info: str, streams: Optional[list] = None, hdr: bool = False):
        super().__init__("trailer", streams, hdr)
        self.__info = info

    @property
    def info(self) -> str:
        """returns trailers movie info"""
        return self.__info

    def make_dict(self, super_dict: Optional[dict] = None, include_streams: bool = True) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["info"] = self.__info
        return super().make_dict(super_dict, include_streams)

    # def get_edit_panel(self, ffprobe=None):
    #     '''returns the edit panel'''
    #     section_html = self._title_html("Trailer")
    #     section_html += " " + self._change_section_html("%%TRACKINDEX%%")
    #     section_html += ghtml_parts.hidden(
    #         "track_%%TRACKINDEX%%_video_type", "trailer", True)
    #     section_html += ghtml_parts.item("track_%%TRACKINDEX%%_info", "Information",
    #                                      "Enter trailer information here",
    #                                      ghtml_parts.input_box("text",
    #                                                            "track_%%TRACKINDEX%%_info",
    #                                                            self._info),
    #                                      True)
    #     section_html += super()._get_edit_panel_bottom()
    #     if ffprobe:
    #         section_html += self._make_stream_sections(ffprobe)
    #     return section_html


class OtherTrackType(VideoTrackType):
    """Other Types"""

    def __init__(self, other_type: str, streams: Optional[list] = None, hdr: bool = False):
        super().__init__("other", streams, hdr)
        self.__other_type = other_type

    @property
    def other_type(self) -> str:
        """returns other type"""
        return self.__other_type

    def make_dict(self, super_dict: Optional[dict] = None, include_streams: bool = True) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["other_type"] = self.__other_type
        return super().make_dict(super_dict, include_streams)

    # def get_edit_panel(self, ffprobe=None):
    #     '''returns the edit panel'''
    #     section_html = self._title_html("Other")
    #     section_html += " " + self._change_section_html("%%TRACKINDEX%%")
    #     section_html += ghtml_parts.hidden(
    #         "track_%%TRACKINDEX%%_video_type", "other", True)
    #     section_html += ghtml_parts.item("track_%%TRACKINDEX%%_othertype", "Other Type",
    #                                      "What is it?",
    #                                      ghtml_parts.input_box("text",
    #                                                            "track_%%TRACKINDEX%%_othertype",
    #                                                            self._other_type),
    #                                      True)
    #     section_html += super()._get_edit_panel_bottom()
    #     if ffprobe:
    #         section_html += self._make_stream_sections(ffprobe)
    #     return section_html


def make_track_type(track: Union[str, dict]) -> Optional[VideoTrackType]:
    """transforms the track returned from the DB or API to the classes above"""
    if isinstance(track, str):
        track = json.loads(track)
    streams = []
    if "streams" in track:
        for stream_index, stream in enumerate(track["streams"]):
            temp = stream_type.make_stream_type(stream_index, stream)
            streams.append(temp)

    if track["video_type"] == "dontrip":
        return DONTRIPTrackType(track.get("reason", ""))
    elif track["video_type"] == "movie":
        return MovieTrackType(streams=streams, hdr=track.get("hdr", False))
    elif track["video_type"] == "tvshow":
        return TVShowTrackType(
            track.get("season", ""),
            track.get("episode", ""),
            streams=streams,
            hdr=track.get("hdr", False),
        )
    elif track["video_type"] == "trailer":
        return TrailerTrackType(track.get("info", ""), streams=streams, hdr=track.get("hdr", False))
    elif track["video_type"] == "extra":
        return ExtraTrackType(track.get("name", ""), streams=streams, hdr=track.get("hdr", False))
    elif track["video_type"] == "other":
        return OtherTrackType(
            track.get("other_type", ""), streams=streams, hdr=track.get("hdr", False)
        )
    return None


def make_blank_track_type(track_type_code: str) -> Optional[VideoTrackType]:
    """make the blank track type"""
    if track_type_code.lower() == "dontrip":
        return DONTRIPTrackType("")
    elif track_type_code.lower() == "movie":
        return MovieTrackType()
    elif track_type_code.lower() == "tvshow":
        return TVShowTrackType("", "")
    elif track_type_code.lower() == "trailer":
        return TrailerTrackType("")
    elif track_type_code.lower() == "extra":
        return ExtraTrackType("")
    elif track_type_code.lower() == "other":
        return OtherTrackType("")
    return None
