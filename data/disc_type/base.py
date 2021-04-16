"""disc type information"""
import json
from abc import ABCMeta
from abc import abstractmethod
from typing import Dict
from typing import Optional

from data.video_track_type.base import VideoTrackType
from libs.classproperty import classproperty


class DiscType(metaclass=ABCMeta):
    """Master Disc Type"""

    @classproperty
    def TYPESANDICONS(cls) -> Dict[str, str]:
        """returns a list of types with Font Awsome Free Icons"""
        return {
            "Movie": "film",
            "TV Show": "tv",
            "Home Movie": "users",
            "Music Video": "music",
            "Other": "question",
        }

    def __init__(self, disc_type: str, name: str, tracks: list, language: str, tmdb_id: str):
        self.__disc_type = disc_type if disc_type in self.TYPESANDICONS else ""
        self.__name = name
        self.__tracks = tracks if isinstance(tracks, list) else []
        self.__language = language if len(language) == 2 and isinstance(language, str) else "en"
        self.__tmdb_id = tmdb_id

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
    def tmdb_id(self) -> str:
        """returns the tmdb_id"""
        return self.__tmdb_id

    @property
    def track_types_and_icons(self):
        """returns the list of names and icons for video_track_types"""
        if not hasattr(self, "_track_types"):
            return VideoTrackType.TYPESANDICONS
        return_dict = {}
        for item in self._track_types:
            if item in VideoTrackType.TYPESANDICONS:
                return_dict[item] = VideoTrackType.TYPESANDICONS[item]
        return return_dict

    def set_track(self, track_id, track):
        """sets the tracks"""
        if self.__tracks is not None:
            self.__tracks[track_id] = track

    def set_tracks(self, tracks: list):
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
        super_dict["language"] = self.__language
        super_dict["tmdb_id"] = self.__tmdb_id
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
    def html_create_data(self) -> dict:
        """returns the data for html"""
