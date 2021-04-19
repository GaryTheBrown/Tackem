"""video track type information"""
import json
from abc import ABCMeta
from abc import abstractmethod
from typing import Dict
from typing import Optional

from libs import classproperty


class VideoTrackType(metaclass=ABCMeta):
    """Master Type"""

    @classproperty
    def TYPESANDICONS(cls) -> Dict[str, str]:
        """returns a list of types with Font Awsome Free Icons"""
        return {
            "Dont Rip": "ban",
            "Feature": "film",
            "Episode": "tv",
            "Trailer": "film",
            "Extra": "plus",
            "Music": "music",
            "Home Movie": "users",
            "Other": "plus",
        }

    def __init__(self, track_type: str, title: str = "Track"):
        self.__track_type = track_type if track_type in self.TYPESANDICONS else ""
        self.__title = title

    @property
    def track_type(self) -> str:
        """returns the type"""
        return self.__track_type

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

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["type"] = self.__track_type
        return super_dict

    @abstractmethod
    def html_create_data(self, track_id: int, read_only: bool = False) -> dict:
        """returns the data for html"""
