"""stream type information"""
from typing import Optional

from data.stream_type.base import StreamType


class SubtitleStreamType(StreamType):
    """Other Types"""

    def __init__(
        self,
        stream_index: int,
        forced: bool = False,
        hearing_impaired: bool = False,
        lyrics: bool = False,
        label: str = "",
        duplicate: bool = False,
        comment: bool = False,
    ):
        super().__init__("subtitle", stream_index, label)
        self.__forced = forced
        self.__hearing_impaired = hearing_impaired
        self.__comment = comment
        self.__lyrics = lyrics
        self.__duplicate = duplicate

    @property
    def forced(self) -> bool:
        """return forced"""
        return self.__forced

    @property
    def hearing_impaired(self) -> bool:
        """return hearing_impaired"""
        return self.__hearing_impaired

    @property
    def comment(self) -> bool:
        """return comment"""
        return self.__comment

    @property
    def lyrics(self) -> bool:
        """return lyrics"""
        return self.__lyrics

    @property
    def duplicate(self) -> bool:
        """return if duplicate"""
        return self.__duplicate

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["forced"] = self.__forced
        super_dict["hearing_impaired"] = self.__hearing_impaired
        super_dict["comment"] = self.__comment
        super_dict["lyrics"] = self.__lyrics
        super_dict["duplicate"] = self.__duplicate
        return super().make_dict(super_dict)
