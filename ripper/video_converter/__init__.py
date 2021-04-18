"""Master Section for the Video Converter controller"""
from abc import ABCMeta

from peewee import DoesNotExist

from data.disc_type import make_disc_type
from data.video_track_type import make_track_type
from database.ripper.video_convert import VideoConvertInfo
from database.ripper.video_info import VideoInfo
from libs.file import File
from ripper.ffprobe import FFprobe
from ripper.video_converter.chapters import VideoConverterChapters
from ripper.video_converter.metadata import VideoConverterMetadata
from ripper.video_converter.stream_mapping import VideoConverterStreamMapping
from ripper.video_converter.video import VideoConverterVideo


class VideoConverter(
    VideoConverterChapters,
    VideoConverterMetadata,
    VideoConverterStreamMapping,
    VideoConverterVideo,
    metaclass=ABCMeta,
):
    """Master Section for the Video Converter controller"""

    def run(self):
        """ Loops through the standard converter function"""
        try:
            data = (
                VideoConvertInfo.do_select()
                .join(VideoInfo)
                .where(VideoConvertInfo.id == self._db_id)
                .get()
            )
        except DoesNotExist:
            return

        if not self._thread_run:
            return

        second_run = data.video_converted
        if second_run and data.track_data == {}:
            return

        self._filename = data.filename
        outfile = self._filename.replace(".mkv", "") + ".NEW.mkv"

        self._label = data.label

        if not File.exists(self._filename):
            data.do_delete().execute()
            return
        if File.exists(outfile):
            File.rm(outfile)

        self._command.append(self._conf["ffmpeglocation"].value)
        self._command.append("-i")
        self._command.append(f'"{self._filename}"')

        auto_mode = False
        if data.track_data == {}:
            self.__create_convert_command_no_info()
        else:
            self.__create_convert_command_with_info(data)
            if not second_run:
                auto_mode = True
        self._command.append(f'"{outfile}"')

        if not self._convert:
            if auto_mode or second_run:
                pass
                data.do_delete().execute()
                self.__pass_single_to_library()
            return

        if not self._thread_run:
            return
        with self._pool_sema:
            if not self._thread_run:
                return
            self._get_frame_count(self._filename)
            if self._do_conversion():
                File.move(self._filename, self._filename + ".OLD")
                File.move(outfile, self._filename)
                File.rm(self._filename + ".OLD")
                if second_run or auto_mode:
                    data.do_delete().execute()
                    self.__pass_single_to_library()
                else:
                    data.video_converted = True
                    data.save()

    def __create_convert_command_no_info(self):
        """creates the conversion command here"""
        probe_info = FFprobe(self._conf["ffprobelocation"].value, self._filename)
        self._command.append("-map_metadata 0")
        self._command.append("-map_chapters 0")
        self._command.append("-map 0")
        self._sort_video_data(probe_info)
        self._command.append("-c:a copy")
        self._command.append("-c:s copy")

    def __create_convert_command_with_info(self, data: VideoConvertInfo):
        """creates the conversion command here"""
        disc_info = make_disc_type(data.disc_info.rip_data)
        track_data = make_track_type(data.track_data)
        probe_info = FFprobe(self._conf["ffprobelocation"].value, self._filename)
        self._sort_metadata(disc_info, track_data)
        self._sort_chapters(probe_info)
        self._sort_stream_mapping(track_data, probe_info)
        if data.video_converted:
            self._command.append("-c:v copy")
        else:
            self._sort_video_data(probe_info)
        self._command.append("-c:a copy")
        self._command.append("-c:s copy")

    def __pass_single_to_library(self):
        """passes the file to the library with its information"""
        # TODO write this function to pass the file to the Labrary.
        pass
