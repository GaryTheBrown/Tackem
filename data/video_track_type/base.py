"""video track type information"""
import json
from abc import ABCMeta
from typing import Dict
from typing import Optional

from libs.classproperty import classproperty


class VideoTrackType(metaclass=ABCMeta):
    """Master Type"""

    @classproperty
    def TYPESANDICONS(cls) -> Dict[str, str]:
        """returns a list of types with Font Awsome Free Icons"""
        return {
            "dontrip": "ban",
            "feature": "film",
            "episode": "tv",
            "trailer": "film",
            "extra": "plus",
            "other": "plus",
        }

    def __init__(self, video_type: str, streams: Optional[list], title: str = "Track"):
        self.__video_type = video_type if video_type in self.TYPESANDICONS else ""
        self.__streams = streams if isinstance(streams, list) else []
        self.__title = title

    @property
    def video_type(self) -> str:
        """returns the type"""
        return self.__video_type

    @property
    def streams(self) -> list:
        """returns streams"""
        return self.__streams

    @property
    def title(self) -> list:
        """returns title"""
        return self.__title

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
        return super_dict

    def _change_section_html(self, track: str) -> str:
        """change section code"""
        html = '<div class="onclick topright" onclick="tracktype(' + str(track)
        html += ", 'change');\">(change)</div>"
        return html
