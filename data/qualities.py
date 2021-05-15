"""Quality Info"""
from typing import List
from typing import Optional

from libs import classproperty


class Quality:
    """Single Quality"""

    def __init__(self, resolution: str, quality: str):
        self.__resolution = resolution
        self.__quality = quality

    @property
    def var_name(self):
        """returns variable name"""
        q = self.__resolution.lower()
        r = self.__quality.replace(" ", "").lower()
        return q + r

    @property
    def name(self):
        """Returns Name"""
        return f"{self.__resolution} - {self.__quality}"

    @property
    def resolution(self):
        """Returns Resolutions"""
        return self.__resolution

    @property
    def quality(self):
        """Returns Quality"""
        return self.__quality


class Qualities:

    __data = [
        Quality("720p", "HDTV"),
        Quality("1080p", "HDTV"),
        Quality("720p", "WEBRip"),
        Quality("720p", "WEBDL"),
        Quality("720p", "Bluray"),
        Quality("1080p", "WEBRip"),
        Quality("1080p", "WEBDL"),
        Quality("1080p", "Bluray"),
        Quality("1080p", "Bluray Remux"),
        Quality("2160p", "HDTV"),
        Quality("2160p", "WebRip"),
        Quality("2160p", "WebDL"),
        Quality("2160p", "Bluray"),
        Quality("2160p", "Bluray Remux"),
    ]

    @classproperty
    def all(cls) -> List[Quality]:
        """returns qualities"""
        return cls.__data

    @classmethod
    def config_option(cls, obj, first: int = 0, last: int = -1):
        """returns a list of 2 letter codes"""
        return [obj(x.var_name, x.name) for x in cls.__data[first:last]]

    @classmethod
    def config_values(cls, first: int = 0, last: int = -1) -> List[str]:
        """returns a list of all values"""
        return [x.var_name for x in cls.__data[first:last]]

    @classmethod
    def by_resolution(cls, resolution) -> List[Quality]:
        """returns a list of qualities filtered by a resolution"""
        return [x for x in cls.__data if x.resolution == resolution]

    @classmethod
    def by_quality(cls, quality) -> List[Quality]:
        """returns a list of qualities filtered by a quality"""
        return [x for x in cls.__data if x.quality == quality]

    @classmethod
    def get(cls, resolution: str, quality: str) -> Optional[Quality]:
        """returns a list of qualities filtered by a quality"""
        for q in cls.__data:
            if q.quality == quality and q.resolution == resolution:
                return q
        return None
