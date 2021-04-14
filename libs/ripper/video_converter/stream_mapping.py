"""Video Controller Stream Mapping code"""
from data.video_track_type.base import VideoTrackType
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

    def __map_stream(self, probe_info: FFprobe, index: int):
        """system to return if to map the stream"""
        stream_info = probe_info.get_stream(index)
        stream_type = stream_info.get("codec_type")
        stream_language = stream_info.get("tags", {}).get("language", "eng")
        stream_format = stream_info.get("codec_name", "")
        if stream_type == "video":
            return True
        if stream_type == "audio":
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
        elif stream_type == "subtitle":
            if self._conf["subtitles"]["subtitle"].value == "all":
                return True
            if self._conf["subtitles"]["subtitle"].value == "selected":
                if stream_language in self._conf["subtitles"]["subtitlelanguages"].value:
                    return True
        return False
