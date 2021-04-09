"""stream type information"""
import json
from abc import ABCMeta
from typing import Optional


class StreamType(metaclass=ABCMeta):
    """Master Type"""

    _types = ["video", "audio", "subtitle"]

    def __init__(self, stream_type: str, stream_index: int, label: str):
        self.__stream_type = stream_type if stream_type in self._types else ""
        self.__stream_index = stream_index
        self.__label = label

    @property
    def stream_type(self) -> str:
        """returns the type"""
        return self.__stream_type

    @property
    def stream_index(self) -> int:
        """returns the index"""
        return self.__stream_index

    @property
    def label(self) -> str:
        """return label"""
        return self.__label

    def json(self) -> str:
        """returns the Stream Type as a Json String"""
        return json.dumps(self.make_dict())

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["stream_type"] = self.__stream_type
        super_dict["label"] = self.__label
        return super_dict

    @property
    def _var_start(self) -> str:
        """returns the variable name start"""
        return "track_%%TRACKINDEX%%_stream_" + str(self.__stream_index) + "_"
