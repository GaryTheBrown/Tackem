'''Master Section for the Video Converter controller'''
from threading import BoundedSemaphore
import threading
import os
import os.path
import pexpect
from libs.database import Database
from libs.database.messages import SQLSelect, SQLUpdate
from libs.database.where import Where
from libs.file import File
from libs.scraper import Scraper
from data.languages import Languages
from data.config import CONFIG
from data.database.ripper import VIDEO_CONVERT_DB
from libs.ripper.ffprobe import FFprobe
from presets import get_video_preset_command

#TODO HDR Support need to use bellow info to check the file for HDR and if it is then make sure the
# system forces x265 mode.
#split the converter settings up so we can give different options for SD HD UHD and HDR
# https://codecalamity.com/encoding-uhd-4k-hdr10-videos-with-ffmpeg/
# https://www.maxvergelli.com/how-to-convert-hdr10-videos-to-sdr-for-non-hdr-devices/
# https://github.com/lasinger/3DVideos2Stereo

class VideoConverter():
    '''Master Section for the Video Converter controller'''

    def __init__(self, pool_sema: BoundedSemaphore, db_id: int):
        self.__thread = threading.Thread(target=self.run, args=())
        self.__thread.setName(f"Converter Task: {str(db_id)}")

        self.__pool_sema = pool_sema
        self.__db_id = db_id

        self.__conf = CONFIG['ripper']['converter']
        self.__infile: str = ""
        self.__outfile: str = ""
        self.__disc_language: str = ""
        self.__probe_info: dict = {}
        self.__command: list = []
        self.__frame_count: int = 0
        self.__frame_process: int = 0
        self.__percent: float = 0.0

        self.__active: bool = False
        self.__thread_run: bool = True
        self.__thread.start()

    @property
    def thread_run(self) -> bool:
        '''return if thread is running'''
        return self._thread.is_alive()

    @property
    def active(self) -> bool:
        '''return if thread is Active'''
        return self.__active

    def stop_thread(self):
        '''stop the thread'''
        if self.__thread.is_alive():
            self.__thread_run = False
            self.__thread.join()

###########
##GETTERS##
###########

    def get_id(self):
        '''returns the ID'''
        return "v" + self._id

    def api_data(self) -> dict:
        '''returns the data as dict for html'''
        file_name_split = self._filename.replace(".mkv", "").split("/")
        return_dict = {
            'id': self._id,
            'discid': int(file_name_split[0]),
            'trackid': int(file_name_split[1]),
            'converting': self.__running,
            'count': self.__frame_count,
            'process': self.__frame_process,
            'percent': self.__percent
        }
        return return_dict

    def converting(self):
        '''return if converting'''
        return self.__running


##########
##Script##
##########
    def run(self):
        ''' Loops through the standard converter function'''

        msg = SQLSelect(VIDEO_CONVERT_DB, Where("id", self.__db_id))
        Database.call(msg)

        if not isinstance(msg.return_data, dict):
            return

        if not self.__thread_run:
            return



        self._id = msg.return_data['id']
        self._filename = msg.return_data['filename']
        self._disc_info = msg.return_data['disc_info']
        self._track_info = msg.return_data['track_info']

        msg = SQLSelect(
            VIDEO_CONVERT_DB,
            Where("id", self._id)
        )
        Database.call(msg)
        self._sql_row_id = msg.return_data['id']
        loc = File.location(CONFIG['ripper']['locations']['videoripping'].value)
        self.__infile = loc + self._filename
        self.__outfile = self.__infile.replace(".mkv", "") + ".NEW.mkv"
        self.__disc_language = Languages().convert_2_to_3t(self._disc_info.language())
        self.__probe_info = FFprobe(self.__conf['ffprobelocation'].value, self.__infile)

        if not self._thread_run:
            return
        with self.__pool_sema:
            if not self._thread_run:
                return
            self._create_command()
            if not self._thread_run:
                return
            self._get_frame_count()
            if self._do_conversion():
                File.move(self.__infile, self.__infile + ".OLD")
                File.move(self.__outfile, self.__infile)
                if not self.__conf['keeporiginalfile'].value:
                    File.rm(self.__infile + ".OLD")

    def _create_command(self):
        '''creates the conversion command here'''
        if not os.path.exists(self.__infile):
            print("ERROR:" + self.__infile + " missing")
            return False  # PROBLEM HERE AS IN FILE MISSING
        if os.path.exists(self.__outfile):
            os.remove(self.__outfile)

        self.__command.append(self.__conf['ffmpeglocation'].value)
        self.__command.append("-i")
        self.__command.append(f'"{self.__infile}"')

        # # Deal with tagging here
        # if self.__conf['video']['videoinserttags'].value:
        #     scraper = Scraper()
        #     disc_type = self._disc_info.disc_type()
        #     track_type = self._track_info.video_type()
        #     tags = []
        #     scraper_data = None
        #     if disc_type == "Movie":
        #         scraper_info = scraper.get_movie_details(
        #             self._disc_info.moviedbid())
        #         if scraper_info['success']:
        #             scraper_data = scraper_info['response']
        #         if track_type == "movie":
        #             tags.append('title="' + self._disc_info.name() + '"')
        #             tags.append('year=' + str(self._disc_info.year()))
        #         elif track_type == "extra":
        #             extra_title = self._disc_info.name() + " (" + str(self._disc_info.year())
        #             extra_title += ") - " + self._track_info.name()
        #             tags.append('title="' + extra_title + '"')
        #         elif track_type == "trailer":
        #             trailer_title = self._disc_info.name() + " (" + str(self._disc_info.year())
        #             trailer_title += ") - " + self._track_info.info()
        #             tags.append('title="' + trailer_title + '"')
        #         elif track_type == "other":
        #             other_title = self._disc_info.name()
        #             other_title += ") - " + self._track_info.other_type()
        #             tags.append('title="' + other_title + '"')
        #     elif disc_type == "TV Show":
        #         tags.append('show="' + self._disc_info.name() + '"')
        #         if track_type == "tvshow":
        #             scraper_info = scraper.get_tvshow_episode_details(self._disc_info.moviedbid(),
        #                                                               self._track_info.season(),
        #                                                               self._track_info.episode())
        #             scraper_data = scraper_info['response']
        #             tags.append('season=' + str(self._track_info.season()))
        #             tags.append('episode=' + str(self._track_info.episode()))
        #             tags.append('title="' + scraper_data['name'] + '"')
        #         elif track_type == "extra":
        #             tags.append('title="' + self._track_info.name() + '"')
        #         elif track_type == "trailer":
        #             tags.append('title="' + self._track_info.info() + '"')
        #         elif track_type == "other":
        #             tags.append(
        #                 'title="' + self._track_info.other_type() + '"')
        #     tags.append('language="' + self._disc_info.language() + '"')

        #     for tag in tags:
        #         self.__command.append('-metadata')
        #         self.__command.append(tag)

        # Deal with chapters here
        if self.__probe_info.has_chapters():
            self.__command.append("-map_chapters")
            if self.__conf['chapters']['keepchapters'].value:
                self.__command.append("0")
            else:
                self.__command.append("-1")

        # Deal with mapping streams here
        streams = self._track_info.streams()
        map_links = [None] * len(streams)
        new_count = 0
        for index, stream in enumerate(streams):
            if self._map_stream(index, stream):
                self.__command.append("-map 0:" + str(index))
                map_links[index] = new_count
                new_count += 1

        # Add metadata and dispositions for each track here
        video_count = 0
        audio_count = 0
        subtitle_count = 0
        for index, stream in enumerate(streams):
            if map_links[index] is not None:
                deposition = self._make_deposition(stream,
                                                   self.__probe_info.get_stream(
                                                       index)["disposition"]
                                                   )
                if stream.stream_type() == "video":
                    if stream.label() != "":
                        self.__command.append(
                            "-metadata:s:v:" + str(video_count))
                        self.__command.append(
                            f'title="[{stream.label()}]"')
                        # self.__command.append('handler="[' + stream.label() + ']"')
                    self.__command.append("-disposition:v:" + str(video_count))
                    self.__command.append(str(deposition))
                    video_count += 1
                elif stream.stream_type() == "audio":
                    if stream.label() != "":
                        self.__command.append(
                            "-metadata:s:a:" + str(audio_count))
                        self.__command.append(
                            f'title="[{stream.label()}]"')
                        # self.__command.append('handler="[' + stream.label() + ']"')
                    self.__command.append("-disposition:a:" + str(audio_count))
                    self.__command.append(str(deposition))
                    audio_count += 1
                elif stream.stream_type() == "subtitle":
                    if stream.label() != "":
                        self.__command.append(
                            "-metadata:s:s:" + str(subtitle_count))
                        self.__command.append(
                            f'title="[{stream.label()}]"')
                        # self.__command.append('handler="[' + stream.label() + ']"')
                    self.__command.append(
                        "-disposition:s:" + str(subtitle_count))
                    self.__command.append(str(deposition))
                    subtitle_count += 1

        # Deal with video resolution here
        config_video_max_height = self.__conf['video']["videoresolution"].value
        video_info = self.__probe_info.get_video_info()
        video_height = video_info[0]['height']

        # Detection of 3d here
        if "stereo_mode" in video_info[0].get("tags", {}):
            if self.__conf['video']['video3dtype'].value != 'keep':
                # 4:3 or 16:9
                aspect_ratio = video_info[0]['display_aspect_ratio']
                type_3d_in = None
                type_3d = video_info[0].get(
                    "tags", {}).get("stereo_mode", "mono")
                if type_3d == 'left_right':
                    # Both views are arranged side by side, Left-eye view is on the left
                    if aspect_ratio == '4:3' or aspect_ratio == '16:9':
                        type_3d_in = 'sbs2l'  # side by side parallel with half width resolution
                    else:
                        type_3d_in = 'sbsl'  # side by side parallel
                elif type_3d == 'right_left':
                    # Both views are arranged side by side, Right-eye view is on the left
                    if aspect_ratio == '4:3' or aspect_ratio == '16:9':
                        type_3d_in = 'sbs2r'  # side by side crosseye with half width resolution
                    else:
                        type_3d_in = 'sbsr'  # side by side crosseye
                elif type_3d == 'bottom_top':
                    #  Both views are arranged in top-bottom orientation, Left-eye view is at bottom
                    if aspect_ratio == '4:3' or aspect_ratio == '16:9':
                        type_3d_in = 'ab2r'  # above-below with half height resolution
                    else:
                        type_3d_in = 'abr'  # above-below
                elif type_3d == 'top_bottom':
                    # Both views are arranged in top-bottom orientation, Left-eye view is on top
                    if aspect_ratio == '4:3' or aspect_ratio == '16:9':
                        type_3d_in = 'ab2l'  # above-below with half height resolution
                    else:
                        type_3d_in = 'abl'  # above-below
                elif type_3d == 'row_interleaved_rl':
                    # Each view is constituted by a row based interleaving, Right-eye view is first
                    type_3d_in = 'irr'
                elif type_3d == 'row_interleaved_lr':
                    # Each view is constituted by a row based interleaving, Left-eye view is first
                    type_3d_in = 'irl'
                elif type_3d == 'col_interleaved_rl':
                    # Both views are arranged in a column based interleaving manner,
                    # Right-eye view is first column
                    type_3d_in = 'icr'
                elif type_3d == 'col_interleaved_lr':
                    # Both views are arranged in a column based interleaving manner,
                    # Left-eye view is first column
                    type_3d_in = 'icl'
                elif type_3d == 'block_lr':
                    # Both eyes laced in one Block, Left-eye view is first alternating frames
                    type_3d_in = 'al'
                elif type_3d == 'block_rl':
                    # Both eyes laced in one Block, Right-eye view is first alternating frames
                    type_3d_in = 'ar'
                if type_3d_in is not None:
                    type_3d_out = self.__conf['video']['video3dtype'].value
                    self.__command.append(
                        f"-vf stereo3d={type_3d_in}:{type_3d_out}")
                    if type_3d_out == "ml" or type_3d_out == "mr":
                        self.__command.append(
                            '-metadata:s:v:0 stereo_mode="mono"')
        if config_video_max_height != "keep":
            if config_video_max_height == "sd":  # 576 or 480
                if video_height > 576:  # PAL spec resolution
                    self.__command.append("-vf scale=-2:480")
            else:  # HD videos Here
                if video_height > config_video_max_height:
                    self.__command.append(
                        "-vf scale=-2:" + config_video_max_height)

        # Deal with video codec here
        if self.__probe_info.is_hdr():
            if self.__conf['video']['hdrmode'].value == "keep":
                self.__command.append('-c:v copy')
            elif self.__conf['video']['hdrmode'].value == "x265default":
                self.__command.append('-c:v libx265')
                #TODO need to DEAL with HDR Magic here
        else:
            if self.__conf['video']['videocodec'].value == "keep":
                self.__command.append('-c:v copy')
            elif self.__conf['video']['videocodec'].value == "x264default":
                self.__command.append('-c:v libx264')
            elif self.__conf['video']['videocodec'].value == "x265default":
                self.__command.append('-c:v libx265')
            elif self.__conf['video']['videocodec'].value == "x264custom":
                self.__command.append('-c:v libx264')
                self.__command.append('-preset')
                self.__command.append(self.__conf['video']['x26preset'].value)
                self.__command.append('-crf')
                if "10le" in video_info[0].get("pix_fmt", ""):
                    self.__command.append(str(self.__conf['video']['x26crf10bit'].value))
                else:
                    self.__command.append(str(self.__conf['video']['x26crf8bit'].value))
                if self.__conf['video']['x26extra'].value:
                    self.__command.append(str(self.__conf['video']['x26extra'].value))
            elif self.__conf['video']['videocodec'].value == "x265custom":
                self.__command.append('-c:v libx265')
                self.__command.append('-preset')
                self.__command.append(self.__conf['video']['x26preset'].value)
                self.__command.append('-crf')
                if "10le" in video_info[0].get("pix_fmt", ""):
                    self.__command.append(str(self.__conf['video']['x26crf10bit'].value))
                else:
                    self.__command.append(str(self.__conf['video']['x26crf8bit'].value))
                if self.__conf['video']['x26extra'].value:
                    self.__command.append(str(self.__conf['video']['x26extra'].value))
            elif self.__conf['video']['videocodec'].value == "preset":
                video_command = get_video_preset_command(
                    self.__conf['video']['videopreset'].value)
                self.__command.append(video_command)

        # tell ffmpeg to copy the audio
        self.__command.append('-c:a copy')

        # tell ffmpeg to copy the subtitles
        self.__command.append('-c:s copy')

        # tell ffmpag the output file
        self.__command.append(f'"{self.__outfile}"')
        return True

    def _map_stream(self, index, stream):
        '''system to return if to map the stream'''
        stream_info = self.__probe_info.get_stream(index)
        stream_language = stream_info.get("tags", {}).get("language", "eng")
        stream_format = stream_info.get("codec_name", "")
        if stream.stream_type() == "video":
            return True
        if stream.stream_type() == "audio":
            if stream.duplicate():
                return False
            if self.__conf['audio']["audiolanguage"].value == "all":
                if self.__conf['audio']["audioformat"].value == "all":
                    return True
                if self.__conf['audio']["audioformat"].value == "highest":
                    # TODO work out how to detect this
                    pass
                elif self.__conf['audio']["audioformat"].value == "selected":
                    if stream_format in self.__conf['audio']['audioformats'].value:
                        return True
            elif self.__conf['audio']["audiolanguage"].value == "original":
                if stream_language == self.__disc_language:
                    if self.__conf['audio']["audioformat"].value == "all":
                        return True
                    if self.__conf['audio']["audioformat"].value == "highest":
                        # TODO work out how to detect this
                        pass
                    elif self.__conf['audio']["audioformat"].value == "selected":
                        if stream_format in self.__conf['audio']['audioformats'].value:
                            return True
            elif self.__conf['audio']["audiolanguage"].value == "selectedandoriginal":
                original_bool = stream_language == self.__disc_language
                selected_bool = stream_language in self.__conf['audio']['audiolanguages'].value
                if original_bool or selected_bool:
                    if self.__conf['audio']["audioformat"].value == "all":
                        return True
                    if self.__conf['audio']["audioformat"].value == "highest":
                        # TODO work out how to detect this
                        pass
                    elif self.__conf['audio']["audioformat"].value == "selected":
                        if stream_format in self.__conf['audio']['audioformats'].value:
                            return True
            elif self.__conf['audio']["audiolanguage"].value == "selected":
                if stream_language in self.__conf['audio']['audiolanguages'].value:
                    if self.__conf['audio']["audioformat"].value == "all":
                        return True
                    if self.__conf['audio']["audioformat"].value == "highest":
                        # TODO work out how to detect this
                        pass
                    elif self.__conf['audio']["audioformat"].value == "selected":
                        if stream_format in self.__conf['audio']['audioformats'].value:
                            return True
        elif stream.stream_type() == "subtitle":
            if stream.duplicate():
                return False
            if stream.hearing_impaired() is True:
                if self.__conf['subtitles']['keepclosedcaptions'].value:
                    if self.__conf['subtitles']["subtitle"].value == "all":
                        return True
                    if self.__conf['subtitles']["subtitle"].value == "selected":
                        if stream_language in self.__conf['subtitlelanguages'].value:
                            return True
            elif stream.comment() is True:
                if self.__conf['audio']['keepcommentary'].value:
                    if self.__conf['subtitles']["subtitle"].value == "all":
                        return True
                    if self.__conf['subtitles']["subtitle"].value == "selected":
                        if stream_language in self.__conf['subtitles']['subtitlelanguages'].value:
                            return True
            else:
                if self.__conf['subtitles']["subtitle"].value == "all":
                    return True
                if self.__conf['subtitles']["subtitle"].value == "selected":
                    if stream_language in self.__conf['subtitles']['subtitlelanguages'].value:
                        return True
        return False

    def _make_deposition(self, stream, ffprobe_data):
        '''creates deposition value'''
        result = 0
        try:
            if stream.default():
                result += 1
        except AttributeError:
            if ffprobe_data['default'] == 1:
                result += 1
        try:
            if stream.dub():
                result += 2
        except AttributeError:
            if ffprobe_data['dub'] == 1:
                result += 2
        try:
            if stream.original():
                result += 4
        except AttributeError:
            if ffprobe_data['original'] == 1:
                result += 4
        try:
            if stream.comment():
                result += 8
        except AttributeError:
            if ffprobe_data['comment'] == 1:
                result += 8
        try:
            if stream.lyrics():
                result += 16
        except AttributeError:
            if ffprobe_data['lyrics'] == 1:
                result += 16
        try:
            if stream.karaoke():
                result += 32
        except AttributeError:
            if ffprobe_data['karaoke'] == 1:
                result += 32
        try:
            if stream.forced():
                result += 64
        except AttributeError:
            if ffprobe_data['forced'] == 1:
                result += 64
        try:
            if stream.hearing_impaired():
                result += 128
        except AttributeError:
            if ffprobe_data['hearing_impaired'] == 1:
                result += 128
        try:
            if stream.visual_impaired():
                result += 256
        except AttributeError:
            if ffprobe_data['visual_impaired'] == 1:
                result += 256
        return result

    def _get_frame_count(self):
        '''gets the frame count of the file'''
        cmd = 'ffmpeg -hide_banner -v quiet -stats -i "'
        cmd += self.__infile
        cmd += '" -map 0:v:0 -c copy -f null -'
        frames = 0
        thread = pexpect.spawn(cmd, encoding='utf-8')
        cpl = thread.compile_pattern_list([pexpect.EOF, "frame= *\d+"])
        while True:
            i = thread.expect_list(cpl, timeout=None)
            if i == 0:  # EOF
                break
            elif i == 1:
                frames = thread.match.group(0)
        self.__frame_count = int(frames.replace("frame=", "").strip())

    def _do_conversion(self):
        '''method to convert file'''
        self.__running = True
        thread = pexpect.spawn(" ".join(self.__command), encoding='utf-8')
        cpl = thread.compile_pattern_list([pexpect.EOF, "frame= *\d+"])
        while True:
            i = thread.expect_list(cpl, timeout=None)
            if i == 0:  # EOF
                self.__running = False
                return True
            if i == 1:
                return_string = thread.match.group(0).replace("frame=", "").lstrip()
                self.__frame_process = int(return_string)
                self.__percent = round(
                    float(self.__frame_process / self.__frame_count * 100), 2)
