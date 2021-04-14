"""video track type information"""
import json
from typing import Optional
from typing import Union

from data.video_track_type.base import VideoTrackType
from data.video_track_type.dontrip import DONTRIPTrackType
from data.video_track_type.episode import EpisodeTrackType
from data.video_track_type.extra import ExtraTrackType
from data.video_track_type.feature import FeatureTrackType
from data.video_track_type.homemovie import HomeMovieTrackType
from data.video_track_type.music import MusicTrackType
from data.video_track_type.other import OtherTrackType
from data.video_track_type.trailer import TrailerTrackType


def make_track_type(track: Union[str, dict]) -> Optional[VideoTrackType]:
    """transforms the track returned from the DB or API to the classes above"""
    if isinstance(track, str):
        track = json.loads(track)

    if track["video_type"] == "dontrip":
        return DONTRIPTrackType(track.get("reason", ""))
    if track["video_type"] == "feature":
        return FeatureTrackType()
    if track["video_type"] == "episode":
        return EpisodeTrackType(track.get("season", ""), track.get("episode", ""))
    if track["video_type"] == "trailer":
        return TrailerTrackType(track.get("info", ""))
    if track["video_type"] == "extra":
        return ExtraTrackType(track.get("name", ""))
    if track["video_type"] == "music":
        return MusicTrackType(track.get("name", ""))
    if track["video_type"] == "other":
        return OtherTrackType(track.get("name", ""))
    if track["video_type"] == "homemovie":
        return HomeMovieTrackType(track.get("name", ""))
    return None


def make_blank_track_type(track_type_code: str) -> Optional[VideoTrackType]:
    """make the blank track type"""
    if track_type_code.lower() == "dontrip":
        return DONTRIPTrackType("")
    if track_type_code.lower() == "feature":
        return FeatureTrackType()
    if track_type_code.lower() == "episode":
        return EpisodeTrackType("", "")
    if track_type_code.lower() == "trailer":
        return TrailerTrackType("")
    if track_type_code.lower() == "extra":
        return ExtraTrackType("")
    if track_type_code.lower() == "music":
        return MusicTrackType("")
    if track_type_code.lower() == "homemovie":
        return HomeMovieTrackType("")
    if track_type_code.lower() == "other":
        return OtherTrackType("")
    return None
