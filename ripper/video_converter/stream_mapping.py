"""Video Controller Stream Mapping code"""
from ripper.video_converter.base import VideoConverterBase


class VideoConverterStreamMapping(VideoConverterBase):
    """Video Controller Stream Mapping code"""

    def _sort_stream_mapping(self, track_data: dict):
        """sorts out the stream mapping"""

        # Deal with mapping streams here
        map_links = [None] * len(track_data["streams"])
        new_count = 0
        for index, stream in enumerate(track_data["streams"]):
            if self.__map_stream(stream):
                self._command.append("-map 0:" + str(index))
                map_links[index] = new_count
                new_count += 1

    # TODO Fix this with the new data possably find the correct codec ID for them tracks and put
    # them in data.audio_format_options
    def __map_stream(self, stream_data: dict):
        """system to return if to map the stream"""
        stream_language = stream_data["LangCode"]
        stream_format = ""  # todo get from stream_data
        if stream_data["Type"] == "Video":
            return True
        if stream_data["Type"] == "Audio":
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
        elif stream_data["Type"] == "Subtitles":
            if self._conf["subtitles"]["subtitle"].value == "all":
                return True
            if self._conf["subtitles"]["subtitle"].value == "selected":
                if stream_language in self._conf["subtitles"]["subtitlelanguages"].value:
                    return True
        return False
