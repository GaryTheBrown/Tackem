"""Master Section for the Video Converter controller"""
from abc import ABCMeta
from libs.ripper.video_converter.chapters import VideoConverterChapters
from libs.ripper.video_converter.stream_mapping import VideoConverterStreamMapping
from libs.ripper.data.video_track_type import make_track_type
from libs.ripper.data.disc_type import make_disc_type
from libs.ripper.ffprobe import FFprobe
import os
from libs.database.messages.delete import SQLDelete
from data.config import CONFIG
from libs.file import File
from libs.database import Database
from libs.database.where import Where
from data.database.ripper import VIDEO_CONVERT_DB
from libs.database.messages.select import SQLSelect
from libs.ripper.video_converter.metadata import VideoConverterMetadata
from libs.ripper.video_converter.video import VideoConverterVideo


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

        msg = SQLSelect(VIDEO_CONVERT_DB, Where("id", self._db_id))
        Database.call(msg)

        if not isinstance(msg.return_data, dict):
            return

        if not self._thread_run:
            return

        self._filename = msg.return_data["filename"]
        infile = File.location(
            CONFIG["ripper"]["locations"]["videoripping"].value + self._filename
        )
        outfile = infile.replace(".mkv", "") + ".NEW.mkv"

        if not os.path.exists(infile):
            print("ERROR:" + infile + " missing")
            return  # PROBLEM HERE AS IN FILE MISSING
        if os.path.exists(outfile):
            os.remove(outfile)

        self._command.append(self._conf["ffmpeglocation"].value)
        self._command.append("-i")
        self._command.append(f'"{infile}"')
        if msg.return_data["disc_info"] == {}:
            self.__create_command_no_info()
        else:
            self.__create_command_with_info(msg.return_data)
        self._command.append(f'"{outfile}"')

        if not self._thread_run:
            return
        with self._pool_sema:
            if not self._thread_run:
                return
            self._get_frame_count(infile)
            if self._do_conversion():
                File.move(infile, infile + ".OLD")
                File.move(outfile, infile)
                if not self._conf["keeporiginalfile"].value:
                    File.rm(infile + ".OLD")
                Database.call(SQLDelete(VIDEO_CONVERT_DB, Where("id", self.__db_id)))

    def __create_command_no_info(self):
        """creates the conversion command here"""
        probe_info = FFprobe(
            self._conf["ffprobelocation"].value,
            File.location(
                CONFIG["ripper"]["locations"]["videoripping"].value + self._filename
            ),
        )

        # Copy accross most metadata
        self._command.append("-map_metadata 0")

        # Deal with chapters here
        self._command.append("-map_chapters 0")

        # Deal with mapping all streams here
        self._command.append("-map 0")

        # Deal with video resolution here
        self._sort_video_data(probe_info)

        # tell ffmpeg to copy the audio
        self._command.append("-c:a copy")

        # tell ffmpeg to copy the subtitles
        self._command.append("-c:s copy")

    def __create_command_with_info(self, db_info: dict):
        """creates the conversion command here"""
        disc_info = make_disc_type(db_info["disc_info"])
        track_info = make_track_type(db_info["track_info"])
        probe_info = FFprobe(
            self._conf["ffprobelocation"].value,
            File.location(
                CONFIG["ripper"]["locations"]["videoripping"].value + self._filename
            ),
        )

        # Deal with tagging here
        self._sort_metadata(disc_info, track_info)

        # Deal with chapters here
        self._sort_chapters(probe_info)

        # Deal with mapping streams here
        self._sort_stream_mapping(track_info, probe_info)

        # Deal with the video data
        self._sort_video_data(probe_info)

        # tell ffmpeg to copy the audio
        self._command.append("-c:a copy")

        # tell ffmpeg to copy the subtitles
        self._command.append("-c:s copy")
