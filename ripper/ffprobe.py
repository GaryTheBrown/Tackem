"""ffprobe system"""
import json
from shutil import which
from subprocess import PIPE
from subprocess import Popen
from typing import Optional


class FFprobe:
    """ffprobe system"""

    def __init__(self, ffprob_location, infile):
        self.__infile = infile
        prog_args = [
            which(ffprob_location),
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            infile,
        ]
        process = Popen(prog_args, stdout=PIPE)
        self.__streams = json.loads(process.communicate()[0].decode("utf-8"))["streams"]
        process.wait()

        prog_args = [
            which(ffprob_location),
            "-hide_banner",
            "-loglevel",
            "warning",
            "-select_streams",
            "v",
            "-print_format",
            "json",
            "-show_frames",
            "-read_intervals",
            "%+#1",
            "-show_entries",
            "frame=color_space,color_primaries,color_transfer,side_data_list,pix_fmt",
            "-i",
            infile,
        ]
        process = Popen(prog_args, stdout=PIPE)
        self._hdr_info = json.loads(process.communicate()[0].decode("utf-8"))["frames"][0]
        process.wait()

    def is_hdr(self) -> bool:
        """returns if the video is HDR"""
        return "color_primaries" in self._hdr_info and self._hdr_info["color_primaries"] == "bt2020"

        # TODO more HDR stuff here

    def hdr_settings(self) -> str:
        """generates the x265 params for HDR"""

    # -x265-params
    # hdr-opt=1:repeat-headers=1:colorprim=bt2020:transfer=smpte2084:colormatrix=bt2020nc:
    # master-display=G(8500,39850)
    #                B(6550,2300)
    #                R(35400,14600)
    #                WP(15635,16450)L(40000000,50):max-cll=0,0

    @property
    def streams(self) -> list:
        """returns all the streams"""
        return self.__streams

    def stream(self, index: int) -> Optional[dict]:
        """return a stream"""
        if index <= len(self.__streams):
            return self.__streams[index]
        print(f"{index} <= {len(self.__streams)}")
        return {}

    @property
    def default_language(self) -> str:
        """returns the default language of the track"""
        for stream in self.__streams:
            if stream["codec_type"] == "audio":
                if stream["disposition"]["default"]:
                    return stream["tags"]["language"]
        print(f"Failed to find default Language in file {self.__infile}")
        return "eng"

    def video_info(self) -> list:
        """returns the video stream information"""
        videos = []
        for stream in self.__streams:
            if stream["codec_type"] == "video":
                videos.append(stream)

        return videos
