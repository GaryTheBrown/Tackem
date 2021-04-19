"""Master Section for the Video Converter controller"""
from abc import ABCMeta

from peewee import DoesNotExist

from database.ripper.video_convert import VideoConvertInfo
from database.ripper.video_info import VideoInfo
from libs.file import File
from ripper.video_converter.chapters import VideoConverterChapters
from ripper.video_converter.stream_mapping import VideoConverterStreamMapping
from ripper.video_converter.video import VideoConverterVideo

# TODO Fix this system crashing when data is rip_data is passed in due to "needing Stream Data"


class VideoConverter(
    VideoConverterChapters,
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

        self._filename = data.filename
        outfile = self._filename.replace(".mkv", "") + ".NEW.mkv"

        self._label = data.label

        if not File.exists(self._filename):
            data.do_delete().execute()
            return
        if File.exists(outfile):
            File.rm(outfile)
        track_data = data.disc_info.disc_data["track_info"][data.track_number]
        self._command.append(self._conf["ffmpeglocation"].value)
        self._command.append("-i")
        self._command.append(f'"{self._filename}"')
        self._sort_chapters(track_data["ChapterCount"] > 0)
        self._sort_stream_mapping(track_data)
        self._sort_video_data()
        self._command.append("-c:a copy")
        self._command.append("-c:s copy")
        self._command.append(f'"{outfile}"')

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
                data.do_delete().execute()
                self.__pass_single_to_library()

    def __pass_single_to_library(self):
        """passes the file to the library with its information"""
        # TODO write this function to pass the file to the Labrary.
        pass
