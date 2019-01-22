'''video track type information'''
import json
from .stream_type import StreamType

class VideoTrackType():
    '''Master Type'''
    _types = ["dontrip", "movie", "tvshow", "trailer", "extra", "other"]
    def __init__(self, video_type, streams):
        if video_type in self._types:
            self._video_type = video_type
        if isinstance(streams, list) and all(issubclass(type(x), StreamType) for x in streams):
            self._streams = streams

    def video_type(self):
        '''returns the type'''
        return self._video_type

class DONTRIPTrackType(VideoTrackType):
    '''Other Types'''
    def __init__(self, reason):
        super().__init__("dontrip", None)
        self._reason = reason

    def reason(self):
        '''return the reason not to rip this track'''
        return self._reason

class MovieTrackType(VideoTrackType):
    '''Movie Type'''
    def __init__(self, tvshow_link=None, tvshow_special_number=None, streams=None):
        super().__init__("movie", streams)
        self._tvshow_link = tvshow_link
        self._tvshow_special_number = tvshow_special_number

    def tvshow_link(self):
        '''return the tv show name for linking'''
        return self._tvshow_link

    def tvshow_special_number(self):
        '''return the tv show special number'''
        return self._tvshow_special_number

class TVShowTrackType(VideoTrackType):
    '''TV Show Type'''
    def __init__(self, season_number, episode_number, streams=None):
        super().__init__("tvshow", streams)
        self._season_number = season_number
        self._episode_number = episode_number

    def season_number(self):
        '''returns tv show season number'''
        return self._season_number

    def episode_number(self):
        '''returns tv show episode number'''
        return self._episode_number

class ExtraTrackType(VideoTrackType):
    '''Extra Type'''
    def __init__(self, name, streams=None):
        super().__init__("extra", streams)
        self._name = name

    def name(self):
        '''returns extra name'''
        return self._name

    # def tvshow_link(self):
    #     '''return the tv show name for linking'''
    #     return self._tvshow_link

    # def tvshow_special_number(self):
    #     '''return the tv show special number'''
    #     return self._tvshow_special_number

class TrailerTrackType(VideoTrackType):
    '''trailer Type'''
    def __init__(self, info, streams=None):
        super().__init__("trailer", streams)
        self._info = info

    def info(self):
        '''returns trailers movie info'''
        return self._info

class OtherTrackType(VideoTrackType):
    '''Other Types'''
    def __init__(self, other_type, streams=None):
        super().__init__("other", streams)
        self._other_type = other_type

    def other_type(self):
        '''returns other type'''
        return self._other_type

def make_track_type(track):
    '''transforms the track returned from the DB or API to the classes above'''
    if isinstance(track, str):
        track = json.loads(track)
        if track is None:
            return None
        elif track['video_type'] == "dontrip":
            return DONTRIPTrackType(track['reason'])
        elif track['video_type'] == "movie":
            return MovieTrackType()
        elif track['video_type'] == "tvshow":
            return TVShowTrackType(track['season_number'], track['episode_number'])
        elif track['video_type'] == "trailer":
            return TrailerTrackType(track['info'])
        elif track['video_type'] == "extra":
            return ExtraTrackType(track['name'])
        elif track['video_type'] == "other":
            return OtherTrackType(track['other_type'])
    return None
