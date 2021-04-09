"""stream type information"""
from typing import Optional

from data.stream_type.base import StreamType


class AudioStreamType(StreamType):
    """Other Types"""

    def __init__(
        self,
        stream_index: int,
        dub: bool = False,
        original: bool = False,
        comment: bool = False,
        visual_impaired: bool = False,
        karaoke: bool = False,
        label: str = "",
        duplicate: bool = False,
    ):
        super().__init__("audio", stream_index, label)
        self.__dub = dub
        self.__original = original
        self.__comment = comment
        self.__visual_impaired = visual_impaired
        self.__karaoke = karaoke
        self.__duplicate = duplicate

    @property
    def dub(self) -> bool:
        """return dub"""
        return self.__dub

    @property
    def original(self) -> bool:
        """return original"""
        return self.__original

    @property
    def comment(self) -> bool:
        """return comment"""
        return self.__comment

    @property
    def visual_impaired(self) -> bool:
        """return visual_impaired"""
        return self.__visual_impaired

    @property
    def karaoke(self) -> bool:
        """return karaoke"""
        return self.__karaoke

    @property
    def duplicate(self) -> bool:
        """return if duplicate stream"""
        return self.__duplicate

    def make_dict(self, super_dict: Optional[dict] = None) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["dub"] = self.__dub
        super_dict["original"] = self.__original
        super_dict["comment"] = self.__comment
        super_dict["visual_impaired"] = self.__visual_impaired
        super_dict["karaoke"] = self.__karaoke
        super_dict["duplicate"] = self.__duplicate
        return super().make_dict(super_dict)
