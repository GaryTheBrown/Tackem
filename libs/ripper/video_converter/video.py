"""Video Controller Video code"""
from libs.ripper.ffprobe import FFprobe
from libs.ripper.video_converter.base import VideoConverterBase
from presets import get_video_preset_command

# TODO HDR Support need to use bellow info to check the file for HDR and if it is then make sure the
# system forces x265 mode.
# split the converter settings up so we can give different options for SD HD UHD and HDR
# https://codecalamity.com/encoding-uhd-4k-hdr10-videos-with-ffmpeg/
# https://www.maxvergelli.com/how-to-convert-hdr10-videos-to-sdr-for-non-hdr-devices/
# https://github.com/lasinger/3DVideos2Stereo


class VideoConverterVideo(VideoConverterBase):
    """Video Controller Video code"""

    def _sort_video_data(self, probe_info: FFprobe):
        """sorts out the video info"""
        video_info = probe_info.video_info()[0]
        # Detection of 3d here
        if "stereo_mode" in video_info.get("tags", {}):
            if self._conf["video"]["video3dtype"].value != "keep":
                self._convert = True
                # 4:3 or 16:9
                aspect_ratio = video_info["display_aspect_ratio"]
                type_3d_in = None
                type_3d = video_info.get("tags", {}).get("stereo_mode", "mono")
                if type_3d == "left_right":
                    # Both views are arranged side by side, Left-eye view is on the left
                    if aspect_ratio == "4:3" or aspect_ratio == "16:9":
                        type_3d_in = "sbs2l"  # side by side parallel with half width resolution
                    else:
                        type_3d_in = "sbsl"  # side by side parallel
                elif type_3d == "right_left":
                    # Both views are arranged side by side, Right-eye view is on the left
                    if aspect_ratio == "4:3" or aspect_ratio == "16:9":
                        type_3d_in = "sbs2r"  # side by side crosseye with half width resolution
                    else:
                        type_3d_in = "sbsr"  # side by side crosseye
                elif type_3d == "bottom_top":
                    #  Both views are arranged in top-bottom orientation, Left-eye view is at bottom
                    if aspect_ratio == "4:3" or aspect_ratio == "16:9":
                        type_3d_in = "ab2r"  # above-below with half height resolution
                    else:
                        type_3d_in = "abr"  # above-below
                elif type_3d == "top_bottom":
                    # Both views are arranged in top-bottom orientation, Left-eye view is on top
                    if aspect_ratio == "4:3" or aspect_ratio == "16:9":
                        type_3d_in = "ab2l"  # above-below with half height resolution
                    else:
                        type_3d_in = "abl"  # above-below
                elif type_3d == "row_interleaved_rl":
                    # Each view is constituted by a row based interleaving, Right-eye view is first
                    type_3d_in = "irr"
                elif type_3d == "row_interleaved_lr":
                    # Each view is constituted by a row based interleaving, Left-eye view is first
                    type_3d_in = "irl"
                elif type_3d == "col_interleaved_rl":
                    # Both views are arranged in a column based interleaving manner,
                    # Right-eye view is first column
                    type_3d_in = "icr"
                elif type_3d == "col_interleaved_lr":
                    # Both views are arranged in a column based interleaving manner,
                    # Left-eye view is first column
                    type_3d_in = "icl"
                # These two seem to be the MVC format
                elif type_3d == "block_lr":
                    # Both eyes laced in one Block, Left-eye view is first alternating frames
                    type_3d_in = "al"
                elif type_3d == "block_rl":
                    # Both eyes laced in one Block, Right-eye view is first alternating frames
                    type_3d_in = "ar"
                if type_3d_in is not None:
                    type_3d_out = self._conf["video"]["video3dtype"].value
                    self._command.append(f"-vf stereo3d={type_3d_in}:{type_3d_out}")
                    if type_3d_out == "ml" or type_3d_out == "mr":
                        self._command.append('-metadata:s:v:0 stereo_mode="mono"')
        if self._conf["video"]["videoresolution"].value != "keep":
            self._convert = True
            if self._conf["video"]["videoresolution"].value == "sd":  # 576 or 480
                if video_info["height"] > 576:  # PAL spec resolution
                    self._command.append("-vf scale=-2:480")
            else:  # HD videos Here
                if video_info["height"] > self._conf["video"]["videoresolution"].value:
                    self._command.append(
                        "-vf scale=-2:" + self._conf["video"]["videoresolution"].value
                    )

        # Deal with video codec here
        if probe_info.is_hdr():
            if self._conf["video"]["hdrmode"].value == "keep":
                self._command.append("-c:v copy")
                return

            self._convert = True
            if self._conf["video"]["hdrmode"].value == "x265default":
                self._command.append("-c:v libx265")
                # TODO need to DEAL with HDR Magic here
        else:
            if self._conf["video"]["videocodec"].value == "keep":
                self._command.append("-c:v copy")
                return
            self._convert = True
            if self._conf["video"]["videocodec"].value == "x264default":
                self._command.append("-c:v libx264")
            elif self._conf["video"]["videocodec"].value == "x265default":
                self._command.append("-c:v libx265")
            elif self._conf["video"]["videocodec"].value == "x264custom":
                self._command.append("-c:v libx264")
                self._command.append("-preset")
                self._command.append(self._conf["video"]["x26preset"].value)
                self._command.append("-crf")
                if "10le" in video_info.get("pix_fmt", ""):
                    self._command.append(str(self._conf["video"]["x26crf10bit"].value))
                else:
                    self._command.append(str(self._conf["video"]["x26crf8bit"].value))
                if self._conf["video"]["x26extra"].value:
                    self._command.append(str(self._conf["video"]["x26extra"].value))
            elif self._conf["video"]["videocodec"].value == "x265custom":
                self._command.append("-c:v libx265")
                self._command.append("-preset")
                self._command.append(self._conf["video"]["x26preset"].value)
                self._command.append("-crf")
                if "10le" in video_info.get("pix_fmt", ""):
                    self._command.append(str(self._conf["video"]["x26crf10bit"].value))
                else:
                    self._command.append(str(self._conf["video"]["x26crf8bit"].value))
                if self._conf["video"]["x26extra"].value:
                    self._command.append(str(self._conf["video"]["x26extra"].value))
            elif self._conf["video"]["videocodec"].value == "preset":
                video_command = get_video_preset_command(self._conf["video"]["videopreset"].value)
                self._command.append(video_command)
