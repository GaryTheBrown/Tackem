"""video track type information"""
import json
from typing import Optional
from typing import Union

from data.stream_type import make_stream_type
from data.video_track_type.base import VideoTrackType
from data.video_track_type.dontrip import DONTRIPTrackType
from data.video_track_type.episode import EpisodeTrackType
from data.video_track_type.extra import ExtraTrackType
from data.video_track_type.feature import FeatureTrackType
from data.video_track_type.other import OtherTrackType
from data.video_track_type.trailer import TrailerTrackType


def make_track_type(track: Union[str, dict]) -> Optional[VideoTrackType]:
    """transforms the track returned from the DB or API to the classes above"""
    if isinstance(track, str):
        track = json.loads(track)
    streams = []
    if "streams" in track:
        for stream_index, stream in enumerate(track["streams"]):
            temp = make_stream_type(stream_index, stream)
            streams.append(temp)

    if track["video_type"] == "dontrip":
        return DONTRIPTrackType(track.get("reason", ""))
    elif track["video_type"] == "feature":
        return FeatureTrackType(streams=streams)
    elif track["video_type"] == "episode":
        return EpisodeTrackType(track.get("season", ""), track.get("episode", ""), streams=streams)
    elif track["video_type"] == "trailer":
        return TrailerTrackType(track.get("info", ""), streams=streams)
    elif track["video_type"] == "extra":
        return ExtraTrackType(track.get("name", ""), streams=streams)
    elif track["video_type"] == "other":
        return OtherTrackType(track.get("other_type", ""), streams=streams)
    return None


def make_blank_track_type(track_type_code: str) -> Optional[VideoTrackType]:
    """make the blank track type"""
    if track_type_code.lower() == "dontrip":
        return DONTRIPTrackType("")
    elif track_type_code.lower() == "feature":
        return FeatureTrackType()
    elif track_type_code.lower() == "episode":
        return EpisodeTrackType("", "")
    elif track_type_code.lower() == "trailer":
        return TrailerTrackType("")
    elif track_type_code.lower() == "extra":
        return ExtraTrackType("")
    elif track_type_code.lower() == "other":
        return OtherTrackType("")
    return None
