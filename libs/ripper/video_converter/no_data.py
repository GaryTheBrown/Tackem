'''Master Section for the Video Converter controller'''
from libs.ripper.video_converter.base import VideoConverterBase
from threading import BoundedSemaphore
import threading
import os
import os.path
import pexpect
from libs.database import Database
from libs.database.messages import SQLSelect, SQLDelete
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

class VideoConverterNoData(VideoConverterBase):
    '''Video Converter controller whith no disc info. converting and copying based on settings'''

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

        self._filename = msg.return_data['filename']

        msg = SQLSelect(
            VIDEO_CONVERT_DB,
            Where("id", self._db_id)
        )
        Database.call(msg)
        self._sql_row_id = msg.return_data['id']
        loc = File.location(CONFIG['ripper']['locations']['videoripping'].value)
        infile = loc + self._filename
        outfile = infile.replace(".mkv", "") + ".NEW.mkv"

        if not os.path.exists(infile):
            print("ERROR:" + infile + " missing")
            return # PROBLEM HERE AS IN FILE MISSING
        if os.path.exists(outfile):
            os.remove(outfile)

        self.__command.append(self.__conf['ffmpeglocation'].value)
        self.__command.append("-i")
        self.__command.append(f'"{infile}"')
        self._create_command(infile)
        self.__command.append(f'"{outfile}"')

        if not self._thread_run:
            return
        with self.__pool_sema:
            if not self._thread_run:
                return
            self._get_frame_count()
            if self._do_conversion():
                File.move(infile, infile + ".OLD")
                File.move(outfile, infile)
                if not self.__conf['keeporiginalfile'].value:
                    File.rm(infile + ".OLD")
                Database.call(SQLDelete(VIDEO_CONVERT_DB, Where("id", self.__db_id)))

    def _create_command(self, infile: str):
        '''creates the conversion command here'''
        keep = False
        probe_info = FFprobe(self.__conf['ffprobelocation'].value, infile)

        #Copy accross most metadata
        self.__command.append("-map_metadata 0")

        # Deal with chapters here
        if probe_info.has_chapters():
            self.__command.append("-map_chapters 0")

        # Deal with mapping all streams here
        self.__command.append(f"-map 0")

        # Deal with video resolution here
        config_video_max_height = self.__conf['video']["videoresolution"].value
        video_info = probe_info.video_info()
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
                #These two seem to be the MVC format
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
                        self.__command.append('-metadata:s:v:0 stereo_mode="mono"')
        if config_video_max_height != "keep":
            if config_video_max_height == "sd":  # 576 or 480
                if video_height > 576:  # PAL spec resolution
                    self.__command.append("-vf scale=-2:480")
            else:  # HD videos Here
                if video_height > config_video_max_height:
                    self.__command.append("-vf scale=-2:" + config_video_max_height)
        else:
            keep = True

        # Deal with video codec here
        if probe_info.is_hdr():
            if self.__conf['video']['hdrmode'].value == "keep" and keep:
                return False
            elif self.__conf['video']['hdrmode'].value == "x265default":
                self.__command.append('-c:v libx265')
                #TODO need to DEAL with HDR Magic here
        else:
            if self.__conf['video']['videocodec'].value == "keep" and keep:
                return False
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
                video_command = get_video_preset_command(self.__conf['video']['videopreset'].value)
                self.__command.append(video_command)

        # tell ffmpeg to copy the audio
        self.__command.append('-c:a copy')

        # tell ffmpeg to copy the subtitles
        self.__command.append('-c:s copy')

        return True
