"""Video Controller Stream Mapping code"""
from ripper.ffprobe import FFprobe
from ripper.video_converter.base import VideoConverterBase


class VideoConverterStreamMapping(VideoConverterBase):
    """Video Controller Stream Mapping code"""

    def _sort_stream_mapping(self, track_data: dict, probe_info: FFprobe):
        """sorts out the stream mapping"""

        # Deal with mapping streams here
        map_links = [None] * len(track_data["streams"])
        new_count = 0
        for index, stream in enumerate(track_data["streams"]):

            if self.__map_stream(stream, probe_info.stream(index), probe_info.default_language):
                self._command.append("-map 0:" + str(index))
                map_links[index] = new_count
                new_count += 1

    def __map_stream(self, sd: dict, ps: dict, default_language: str) -> bool:
        """system to return if to map the stream"""

        if sd["Type"] == "Video":
            return self.__ms_video()
        if sd["Type"] == "Audio":
            return self.__ms_audio_lang(
                sd["LangCode"], default_language
            ) and self.__ms_audio_format(ps["codec_name"])
        elif sd["Type"] == "Subtitles":
            return self.__ms_subtitles(sd, default_language)
        return False

    def __ms_video(self) -> bool:
        """system to return if to map the video stream"""
        return True

    def __ms_audio_lang(self, stream_language: str, default_lang: str) -> bool:
        """system to return if to map the audio stream by language"""
        if self._conf["audio"]["audiolanguage"].value == "all":
            return True
        if self._conf["audio"]["audiolanguage"].value == "original":
            return stream_language == default_lang
        elif self._conf["audio"]["audiolanguage"].value == "default":
            return stream_language == self._conf["defaultlanguage"].value
        elif self._conf["audio"]["audiolanguage"].value == "deaultandoriginal":
            return stream_language in [default_lang, self._conf["defaultlanguage"].value]
        elif self._conf["audio"]["audiolanguage"].value == "selectedandoriginal":
            original_bool = stream_language == default_lang
            selected_bool = stream_language in self._conf["audio"]["audiolanguages"].value
            return original_bool or selected_bool
        elif self._conf["audio"]["audiolanguage"].value == "selected":
            return stream_language in self._conf["audio"]["audiolanguages"].value
        return False

    def __ms_audio_format(self, stream_format: str):
        """system to return if to map the audio stream by codec format"""
        if self._conf["audio"]["audioformat"].value == "all":
            return True
        if self._conf["audio"]["audioformat"].value == "highest":
            # TODO work out how to detect this
            pass
        elif self._conf["audio"]["audioformat"].value == "selected":
            return stream_format in self._conf["audio"]["audioformats"].value
        return False

    def __ms_subtitles(self, stream_data: dict, default_lang: str) -> bool:
        """system to return if to map the video stream"""
        stream_language = stream_data["LangCode"]
        if self._conf["subtitles"]["subtitle"].value == "all":
            return True
        if self._conf["subtitles"]["subtitle"].value == "none":
            return False
        if self._conf["subtitles"]["subtitle"].value == "original":
            return stream_language == default_lang
        elif self._conf["subtitles"]["subtitle"].value == "default":
            return stream_language == self._conf["defaultlanguage"].value
        elif self._conf["subtitles"]["subtitle"].value == "deaultandoriginal":
            return stream_language in [default_lang, self._conf["defaultlanguage"].value]
        elif self._conf["subtitles"]["subtitle"].value == "selectedandoriginal":
            original_bool = stream_language == default_lang
            selected_bool = stream_language in self._conf["audio"]["audiolanguages"].value
            return original_bool or selected_bool
        elif self._conf["subtitles"]["subtitle"].value == "selected":
            return stream_language in self._conf["audio"]["audiolanguages"].value

        return False
