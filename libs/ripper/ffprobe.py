'''ffprobe system'''
import json
from subprocess import DEVNULL, PIPE, Popen
from typing import Optional

class FFprobe:
    '''ffprobe system'''

    def __init__(self, ffprob_location, infile):
        prog_args = [
            ffprob_location,
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            "-show_chapters",
            "-show_format",
            infile
        ]
        process = Popen(prog_args, stdout=PIPE, stderr=DEVNULL)
        self._info = json.loads(process.communicate()[0].decode('utf-8'))
        process.wait()

        prog_args = [
            ffprob_location,
            "-hide_banner",
            "-loglevel",
            "warning",
            "-select_streams",
            "v",
            "-print_format",
            "json"
            "-show_frames",
            "-read_intervals",
            '"%+#1"',
            "-show_entries",
            '"frame=color_space,color_primaries,color_transfer,side_data_list,pix_fmt"',
            "-i ",
            infile
        ]
        process = Popen(prog_args, stdout=PIPE, stderr=DEVNULL)
        self._hdr_info = json.loads(process.communicate()[0].decode('utf-8'))['frames'][0]
        process.wait()

    def is_hdr(self) -> bool:
        '''returns if the video is HDR'''
        return 'color_primaries' in self._hdr_info and self._hdr_info['color_primaries'] == "bt2020"

        #TODO more HDR stuff here

    def hdr_settings(self) -> str:
        '''generates the x265 params for HDR'''
#-x265-params hdr-opt=1:repeat-headers=1:colorprim=bt2020:transfer=smpte2084:colormatrix=bt2020nc:
# master-display=G(8500,39850)B(6550,2300)R(35400,14600)WP(15635,16450)L(40000000,50):max-cll=0,0

    def has_chapters(self) -> bool:
        '''returns true if file has chapters'''
        return 'chapters' in self._info and self._info['chapters']

    def stream_count(self) -> int:
        '''returns the stream count'''
        if 'streams' in self._info and self._info['streams']:
            return len(self._info['streams'])
        return 0

    @property
    def streams(self) -> list:
        '''returns all the streams'''
        return self._info.get("streams", [])

    def stream(self, index) -> Optional[dict]:
        '''return a stream'''
        if 'streams' in self._info and self._info['streams']:
            return self._info['streams'][int(index)]
        return None

    def stream_type_count(self) -> Optional[dict]:
        '''returns the stream types and how many'''
        if 'streams' in self._info and self._info['streams']:
            s_types = {}
            for stream in self._info['streams']:
                _type = stream["codec_type"]
                if _type in s_types:
                    s_types[_type] += 1
                else:
                    s_types[_type] = 1
            return s_types
        return None

    def streams_and_types(self) -> list:
        '''returns a list of streams and there types'''
        if 'streams' in self._info and self._info['streams']:
            streams = []
            for stream in self._info['streams']:
                streams.append(stream["codec_type"])
            return streams

    def video_info(self) -> list:
        '''returns the video stream information'''
        videos = []
        if 'streams' in self._info and self._info['streams']:
            for stream in self._info['streams']:
                if stream["codec_type"] == 'video':
                    videos.append(stream)

        return videos

    def audio_info(self) -> list:
        '''returns the audio stream information'''
        audios = []
        if 'streams' in self._info and self._info['streams']:
            for stream in self._info['streams']:
                if stream["codec_type"] == 'audio':
                    audios.append(stream)
        return audios

    def subtitle_info(self) -> list:
        '''returns the subtitle stream information'''
        subtitles = []
        if 'streams' in self._info and self._info['streams']:
            for stream in self._info['streams']:
                if stream["codec_type"] == 'subtitle':
                    subtitles.append(stream)
        return subtitles

    def format_info(self) -> dict:
        '''returns the format information'''
        return self._info['format']
