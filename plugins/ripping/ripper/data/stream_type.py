'''stream type information'''
#TODO add in extra options to mark if track has commentary and the stream number that it is.
#TODO add in forced info as well maybe.
class StreamType():
    '''Master Type'''
    _types = ["video", "audio", "subtitle"]
    def __init__(self, stream_type):
        if stream_type in self._types:
            self._stream_type = stream_type

    def stream_type(self):
        '''returns the type'''
        return self._stream_type

class VideoStreamType(StreamType):
    '''Other Types'''
    def __init__(self, hdr=False):
        super().__init__("video")
        self._hdr = hdr

class AudioStreamType(StreamType):
    '''Other Types'''
    def __init__(self, dub=False, original=False, comment=False, visual_impaired=False,
                 karaoke=False):
        super().__init__("audio")
        self._dub = dub
        self._original = original
        self._comment = comment
        self._visual_impaired = visual_impaired
        self._karaoke = karaoke

class SubtitleStreamType(StreamType):
    '''Other Types'''
    def __init__(self, forced=False, hearing_impaired=False, lyrics=False):
        super().__init__("subtitle")
        self._forced = forced
        self._hearing_impaired = hearing_impaired
        self._lyrics = lyrics
