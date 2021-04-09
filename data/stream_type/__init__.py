"""stream type information"""
import json

from data.stream_type.audio import AudioStreamType
from data.stream_type.base import StreamType
from data.stream_type.subtitle import SubtitleStreamType
from data.stream_type.video import VideoStreamType


def make_stream_type(stream_index: int, stream: str) -> StreamType:
    """transforms the stream returned from the DB or API to the classes above"""
    if isinstance(stream, str):
        stream = json.loads(stream)
    for key in stream:
        if stream[key] == "True":
            stream[key] = True
        if stream[key] == "False":
            stream[key] = False
    if stream is None:
        return None
    elif stream["stream_type"] == "video":
        return VideoStreamType(stream_index)
    elif stream["stream_type"] == "audio":
        return AudioStreamType(
            stream_index,
            dub=stream.get("dub", False),
            original=stream.get("original", False),
            comment=stream.get("comment", False),
            visual_impaired=stream.get("visual_impaired", False),
            karaoke=stream.get("karaoke", False),
            label=stream.get("label", ""),
            duplicate=stream.get("duplicate", ""),
        )
    elif stream["stream_type"] == "subtitle":
        return SubtitleStreamType(
            stream_index,
            forced=stream.get("forced", False),
            hearing_impaired=stream.get("hearing_impaired", False),
            lyrics=stream.get("lyrics", False),
            label=stream.get("label", ""),
            duplicate=stream.get("duplicate", False),
            comment=stream.get("comment", False),
        )
    return None


def make_blank_stream_type(stream_index: int, stream_type_code: str) -> StreamType:
    """make the blank stream type"""
    if stream_type_code.lower() == "video":
        return VideoStreamType(stream_index)
    elif stream_type_code.lower() == "audio":
        return AudioStreamType(stream_index)
    elif stream_type_code.lower() == "subtitle":
        return SubtitleStreamType(stream_index)
    return None
