"""Master Section for the Video Converter controller"""
from abc import ABCMeta

from data.config import CONFIG
from data.database.ripper import VIDEO_CONVERT_DB
from data.database.ripper import VIDEO_INFO_DB
from libs.database import Database
from libs.database.messages.delete import SQLDelete
from libs.database.messages.select import SQLSelect
from libs.database.messages.update import SQLUpdate
from libs.database.where import Where
from libs.file import File
from libs.ripper.data.disc_type import make_disc_type
from libs.ripper.data.video_track_type import make_track_type
from libs.ripper.ffprobe import FFprobe
from libs.ripper.video_converter.chapters import VideoConverterChapters
from libs.ripper.video_converter.metadata import VideoConverterMetadata
from libs.ripper.video_converter.stream_mapping import VideoConverterStreamMapping
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
        infile = File.location(self._filename)
        outfile = infile.replace(".mkv", "") + ".NEW.mkv"

        if not File.exists(infile):
            print("ERROR:" + infile + " missing")
            return  # PROBLEM HERE AS IN FILE MISSING
        if File.exists(outfile):
            File.rm(outfile)

        self._command.append(self._conf["ffmpeglocation"].value)
        self._command.append("-i")
        self._command.append(f'"{infile}"')

        second_run = msg.return_data["video_converted"]
        auto_mode = False
        if second_run:
            if msg.return_data["track_data"] == {}:
                self._wait.wait()
                if not self._thread_run:
                    return
                Database.call(msg)

        if msg.return_data["track_data"] == {}:
            self.__create_convert_command_no_info()
        else:
            self.__create_convert_command_with_info(msg.return_data)
            if not second_run:
                auto_mode = True
        self._command.append(f'"{outfile}"')

        print(" ".join(self._command))

        if not self._convert:
            if auto_mode or second_run:
                pass
                Database.call(SQLDelete(VIDEO_CONVERT_DB, Where("id", self._db_id)))
                self.__pass_single_to_library()
            return

        if not self._thread_run:
            return
        with self._pool_sema:
            if not self._thread_run:
                return
            self._get_frame_count(infile)
            if self._do_conversion():
                File.move(infile, infile + ".OLD")
                File.move(outfile, infile)
                File.rm(infile + ".OLD")
                if second_run or auto_mode:
                    Database.call(SQLDelete(VIDEO_CONVERT_DB, Where("id", self._db_id)))
                    self.__pass_single_to_library()
                else:
                    Database.call(
                        SQLUpdate(
                            VIDEO_CONVERT_DB,
                            Where("id", self._db_id),
                            video_converted=True,
                        )
                    )

    def __create_convert_command_no_info(self):
        """creates the conversion command here"""
        probe_info = FFprobe(
            self._conf["ffprobelocation"].value,
            File.location(CONFIG["ripper"]["locations"]["ripping"].value + self._filename),
        )
        self._command.append("-map_metadata 0")
        self._command.append("-map_chapters 0")
        self._command.append("-map 0")
        self._sort_video_data(probe_info)
        self._command.append("-c:a copy")
        self._command.append("-c:s copy")

    def __create_convert_command_with_info(self, db_info: dict):
        """creates the conversion command here"""
        msg = SQLSelect(VIDEO_INFO_DB, Where("id", db_info["info_id"]))
        Database.call(msg)
        disc_info = make_disc_type(msg.return_data["rip_data"])
        track_data = make_track_type(db_info["track_data"])
        probe_info = FFprobe(self._conf["ffprobelocation"].value, self._filename)
        self._sort_metadata(disc_info, track_data)
        self._sort_chapters(probe_info)
        self._sort_stream_mapping(track_data, probe_info)
        if db_info["video_converted"]:
            self._command.append("-c:v copy")
        else:
            self._sort_video_data(probe_info)
        self._command.append("-c:a copy")
        self._command.append("-c:s copy")

    def __pass_single_to_library(self):
        """passes the file to the library with its information"""
        # TODO write this function to pass the file to the Labrary.
        pass
