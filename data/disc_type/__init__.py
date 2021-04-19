"""disc type information"""
import json
from typing import Union

from data.disc_type.base import DiscType
from data.disc_type.home_movie import HomeMovieDiscType
from data.disc_type.movie import MovieDiscType
from data.disc_type.music_video import MusicVideoDiscType
from data.disc_type.other import OtherDiscType
from data.disc_type.tv_show import TVShowDiscType
from data.video_track_type import make_track_type


def make_disc_type(data: Union[str, dict]) -> DiscType:
    """transforms the data returned from the DB or API to the classes above"""
    if isinstance(data, str):
        data = json.loads(data)
    tracks = []
    if "tracks" in data:
        for track in data["tracks"]:
            tracks.append(make_track_type(track))
    if data["type"].replace(" ", "").lower() == "movie":
        return MovieDiscType(
            data.get("name", ""),
            data.get("year", ""),
            tracks,
            data.get("language", "en"),
            data.get("tmdbid", ""),
        )
    if data["type"].replace(" ", "").lower() == "tvshow":
        return TVShowDiscType(
            data.get("name", ""),
            tracks,
            data.get("language", "en"),
            data.get("tmdbid", ""),
        )
    if data["type"].replace(" ", "").lower() == "musicvideo":
        return MusicVideoDiscType(
            data.get("name", ""),
            data.get("info", ""),
            tracks,
            data.get("language", "en"),
        )
    if data["type"].replace(" ", "").lower() == "homemovie":
        return HomeMovieDiscType(
            data.get("name", ""),
            data.get("info", ""),
            tracks,
            data.get("language", "en"),
        )
    if data["type"].replace(" ", "").lower() == "other":
        return OtherDiscType(
            data.get("name", ""),
            data.get("info", ""),
            tracks,
            data.get("language", "en"),
        )
    return None


def make_blank_disc_type(disc_type_code: str) -> DiscType:
    """make the blank disc type"""
    if disc_type_code.replace(" ", "").lower() == "movie":
        return MovieDiscType("", 0, None, "en", "")
    if disc_type_code.replace(" ", "").lower() == "tvshow":
        return TVShowDiscType("", None, "en", "")
    if disc_type_code.replace(" ", "").lower() == "musicvideo":
        return MusicVideoDiscType("", "", None, "en")
    if disc_type_code.replace(" ", "").lower() == "homemovie":
        return HomeMovieDiscType("", "", None, "en")
    if disc_type_code.replace(" ", "").lower() == "other":
        return OtherDiscType("", "", None, "en")
    return None
