"""Video Controller Stream Mapping code"""
from libs.ripper.data.stream_type import StreamType
from libs.ripper.data.video_track_type import VideoTrackType
from libs.ripper.ffprobe import FFprobe
from libs.ripper.video_converter.base import VideoConverterBase


class VideoConverterStreamMapping(VideoConverterBase):
    """Video Controller Stream Mapping code"""

    def _sort_stream_mapping(self, track_info: VideoTrackType, probe_info: FFprobe):
        """sorts out the stream mapping"""

        # Deal with mapping streams here
        map_links = [None] * len(track_info.streams)
        new_count = 0
        for index, stream in enumerate(track_info.streams):
            if self.__map_stream(probe_info, index, stream):
                self._command.append("-map 0:" + str(index))
                map_links[index] = new_count
                new_count += 1

        # Add metadata and dispositions for each track here
        video_count = 0
        audio_count = 0
        subtitle_count = 0
        for index, stream in enumerate(track_info.streams):
            if map_links[index] is not None:
                deposition = self.__make_deposition(
                    stream, probe_info.get_stream(index)["disposition"]
                )
                if stream.stream_type() == "video":
                    if stream.label != "":
                        self._command.append("-metadata:s:v:" + str(video_count))
                        self._command.append(f'title="[{stream.label}]"')
                        # self._command.append('handler="[' + stream.label + ']"')
                    self._command.append("-disposition:v:" + str(video_count))
                    self._command.append(str(deposition))
                    video_count += 1
                elif stream.stream_type() == "audio":
                    if stream.label != "":
                        self._command.append("-metadata:s:a:" + str(audio_count))
                        self._command.append(f'title="[{stream.label}]"')
                        # self._command.append('handler="[' + stream.label + ']"')
                    self._command.append("-disposition:a:" + str(audio_count))
                    self._command.append(str(deposition))
                    audio_count += 1
                elif stream.stream_type() == "subtitle":
                    if stream.label != "":
                        self._command.append("-metadata:s:s:" + str(subtitle_count))
                        self._command.append(f'title="[{stream.label}]"')
                        # self._command.append('handler="[' + stream.label + ']"')
                    self._command.append("-disposition:s:" + str(subtitle_count))
                    self._command.append(str(deposition))
                    subtitle_count += 1

    def __map_stream(self, probe_info: FFprobe, index: int, stream: StreamType):
        """system to return if to map the stream"""
        stream_info = probe_info.get_stream(index)
        stream_language = stream_info.get("tags", {}).get("language", "eng")
        stream_format = stream_info.get("codec_name", "")
        if stream.stream_type == "video":
            return True
        if stream.stream_type == "audio":
            if stream.duplicate:
                return False
            if self._conf["audio"]["audiolanguage"].value == "all":
                if self._conf["audio"]["audioformat"].value == "all":
                    return True
                if self._conf["audio"]["audioformat"].value == "highest":
                    # TODO work out how to detect this
                    pass
                elif self._conf["audio"]["audioformat"].value == "selected":
                    if stream_format in self._conf["audio"]["audioformats"].value:
                        return True
            elif self._conf["audio"]["audiolanguage"].value == "original":
                if stream_language == self.__disc_language:
                    if self._conf["audio"]["audioformat"].value == "all":
                        return True
                    if self._conf["audio"]["audioformat"].value == "highest":
                        # TODO work out how to detect this
                        pass
                    elif self._conf["audio"]["audioformat"].value == "selected":
                        if stream_format in self._conf["audio"]["audioformats"].value:
                            return True
            elif self._conf["audio"]["audiolanguage"].value == "selectedandoriginal":
                original_bool = stream_language == self.__disc_language
                selected_bool = stream_language in self._conf["audio"]["audiolanguages"].value
                if original_bool or selected_bool:
                    if self._conf["audio"]["audioformat"].value == "all":
                        return True
                    if self._conf["audio"]["audioformat"].value == "highest":
                        # TODO work out how to detect this
                        pass
                    elif self._conf["audio"]["audioformat"].value == "selected":
                        if stream_format in self._conf["audio"]["audioformats"].value:
                            return True
            elif self._conf["audio"]["audiolanguage"].value == "selected":
                if stream_language in self._conf["audio"]["audiolanguages"].value:
                    if self._conf["audio"]["audioformat"].value == "all":
                        return True
                    if self._conf["audio"]["audioformat"].value == "highest":
                        # TODO work out how to detect this
                        pass
                    elif self._conf["audio"]["audioformat"].value == "selected":
                        if stream_format in self._conf["audio"]["audioformats"].value:
                            return True
        elif stream.stream_type == "subtitle":
            if stream.duplicate:
                return False
            if stream.hearing_impaired is True:
                if self._conf["subtitles"]["keepclosedcaptions"].value:
                    if self._conf["subtitles"]["subtitle"].value == "all":
                        return True
                    if self._conf["subtitles"]["subtitle"].value == "selected":
                        if stream_language in self._conf["subtitlelanguages"].value:
                            return True
            elif stream.comment is True:
                if self._conf["audio"]["keepcommentary"].value:
                    if self._conf["subtitles"]["subtitle"].value == "all":
                        return True
                    if self._conf["subtitles"]["subtitle"].value == "selected":
                        if stream_language in self._conf["subtitles"]["subtitlelanguages"].value:
                            return True
            else:
                if self._conf["subtitles"]["subtitle"].value == "all":
                    return True
                if self._conf["subtitles"]["subtitle"].value == "selected":
                    if stream_language in self._conf["subtitles"]["subtitlelanguages"].value:
                        return True
        return False

    def __make_deposition(self, stream: StreamType, ffprobe_data: FFprobe):
        """creates deposition value"""
        result = 0
        try:
            if stream.default:
                result += 1
        except AttributeError:
            if ffprobe_data["default"] == 1:
                result += 1
        try:
            if stream.dub:
                result += 2
        except AttributeError:
            if ffprobe_data["dub"] == 1:
                result += 2
        try:
            if stream.original:
                result += 4
        except AttributeError:
            if ffprobe_data["original"] == 1:
                result += 4
        try:
            if stream.comment:
                result += 8
        except AttributeError:
            if ffprobe_data["comment"] == 1:
                result += 8
        try:
            if stream.lyrics:
                result += 16
        except AttributeError:
            if ffprobe_data["lyrics"] == 1:
                result += 16
        try:
            if stream.karaoke:
                result += 32
        except AttributeError:
            if ffprobe_data["karaoke"] == 1:
                result += 32
        try:
            if stream.forced:
                result += 64
        except AttributeError:
            if ffprobe_data["forced"] == 1:
                result += 64
        try:
            if stream.hearing_impaired:
                result += 128
        except AttributeError:
            if ffprobe_data["hearing_impaired"] == 1:
                result += 128
        try:
            if stream.visual_impaired:
                result += 256
        except AttributeError:
            if ffprobe_data["visual_impaired"] == 1:
                result += 256
        return result
