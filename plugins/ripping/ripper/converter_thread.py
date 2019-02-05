'''Master Section for the Converter controller'''
import threading
import os
import os.path
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.scraper.scraper_base import Scraper
from libs.data.languages import Languages
from .data.db_tables import VIDEO_CONVERT_DB_INFO as CONVERT_DB
from .ffprobe import FFprobe

class ConverterThread():
    '''Master Section for the Converter controller'''
    def __init__(self, item, config, root_config, db, tasks_sema):
        self._id = item['id']
        self._filename = item['filename']
        self._disc_info = item['disc_info']
        self._track_info = item['track_info']
        self._config = config
        self._root_config = root_config
        self._db = db
        self._tasks_sema = tasks_sema
        self._thread = threading.Thread(target=self.run, args=())
        self._thread_name = "Converter Task " + str(self._id)
        self._thread.setName(self._thread_name)
        self._thread_run = False
        self._task_done = False
        self._sql_row_id = self._db.table_has_row(self._thread_name, CONVERT_DB["name"],
                                                  {"id":self._id})
        temp_location = self._config['locations']['videoripping']
        if temp_location[0] != "/":
            temp_location = PROGRAMCONFIGLOCATION + self._config['locations']['videoripping']
        self._infile = temp_location + self._filename
        self._outfile = temp_location + self._filename.replace(".mkv", "") + ".NEW.mkv"
        self._disc_language = Languages().convert_2_to_3t(self._disc_info.language())
        self._conf = self._config['converter']
        self._probe_info = FFprobe(self._conf['ffprobelocation'], self._infile)
        self._command = []

    def task_done(self):
        '''returns if the task is done'''
        return self._task_done

###########
##GETTERS##
###########

    def get_id(self):
        '''returns the ID'''
        return self._id

    def get_quick_data(self):
        '''returns the data as dict for html'''
        file_name_split = self._filename.replace(".mkv", "").split("/")
        return_dict = {
            'id': self._id,
            'discid': int(file_name_split[0]),
            'trackid': int(file_name_split[1])
        }
        return return_dict

##########
##Thread##
##########
    def start_thread(self):
        '''start the thread'''
        self._thread_run = True
        self._thread.start()

    def stop_thread(self):
        '''stop the thread'''
        if self._thread.is_alive():
            self._thread_run = False
            self._thread.join()

##########
##Script##
##########
    def run(self):
        ''' Loops through the standard converter function'''
        self._tasks_sema.acquire()
        if not self._thread_run:
            self._tasks_sema.release()
            return
        if self._create_command() is not True:
            self._thread_run = False
        if not self._thread_run:
            self._tasks_sema.release()
            return
        print(" ".join(self._command))
        #run converter here with above command
        self._task_done = True
        self._tasks_sema.release()

    def _create_command(self):
        '''creates the conversion command here'''
                #actions here

        if not os.path.exists(self._infile):
            print("ERROR:" + self._infile + " missing")
            return False# PROBLEM HERE AS IN FILE MISSING
        if os.path.exists(self._outfile):
            os.remove(self._outfile)

        self._command.append(self._conf['ffmpeglocation'])
        self._command.append("-i")
        self._command.append('"' + self._infile + '"')

        #Deal with tagging here
        #https://kodi.wiki/view/Video_file_tagging#Title
        if self._conf['videoinserttags']:
            scraper = Scraper(self._root_config)
            disc_type = self._disc_info.disc_type()
            track_type = self._track_info.video_type()
            tags = []
            scraper_data = None
            if disc_type == "Movie":
                scraper_info = scraper.get_movie_details(self._disc_info.moviedbid())
                if scraper_info['success']:
                    scraper_data = scraper_info['response']
                if track_type == "movie":
                    tags.append('title="' + self._disc_info.name() + '"')
                    tags.append('year=' + str(self._disc_info.year()))
                elif track_type == "extra":
                    extra_title = self._disc_info.name() + " (" + str(self._disc_info.year())
                    extra_title += ") - " + self._track_info.name()
                    tags.append('title="' + extra_title + '"')
                elif track_type == "trailer":
                    trailer_title = self._disc_info.name() + " (" + str(self._disc_info.year())
                    extra_title += ") - " + self._track_info.info()
                    tags.append('title="' + trailer_title + '"')
                elif track_type == "other":
                    other_title = self._disc_info.name()
                    extra_title += ") - " + self._track_info.other_type()
                    tags.append('title="' + other_title + '"')
            elif disc_type == "TV Show":
                tags.append('show="' + self._disc_info.name() + '"')
                if track_type == "tvshow":
                    scraper_info = scraper.get_tvshow_episode_details(self._disc_info.moviedbid(),
                                                                      self._track_info.season(),
                                                                      self._track_info.episode())
                    scraper_data = scraper_info['response']
                    tags.append('season=' + str(self._track_info.season()))
                    tags.append('episode=' + str(self._track_info.episode()))
                    tags.append('title="' + scraper_data['name'] + '"')
                elif track_type == "extra":
                    tags.append('title="' + self._track_info.name() + '"')
                elif track_type == "trailer":
                    tags.append('title="' + self._track_info.info() + '"')
                elif track_type == "other":
                    tags.append('title="' + self._track_info.other_type() + '"')
            tags.append('language="' + self._disc_info.language() + '"')

            for tag in tags:
                self._command.append('-metadata')
                self._command.append(tag)

        #Deal with chapters here
        if self._probe_info.has_chapters():
            self._command.append("-map_chapters")
            if self._conf['keepchapters']:
                self._command.append("0")
            else:
                self._command.append("-1")

        #Deal with mapping streams here
        streams = self._track_info.streams()
        map_links = [None] * len(streams)
        new_count = 0
        for index, stream in enumerate(streams):
            if self._map_stream(index, stream):
                self._command.append("-map")
                self._command.append("0:" + str(index))
                map_links[index] = new_count
                new_count += 1

        video_count = 0
        audio_count = 0
        subtitle_count = 0
        for index, stream in enumerate(streams):
            if map_links[index] is not None:
                deposition = self._make_deposition(stream,
                                                   self._probe_info.get_stream(index)["disposition"]
                                                  )
                if stream.stream_type() == "video":
                    if stream.label() != "":
                        self._command.append("-metadata:v:" + str(video_count))
                        self._command.append('title="[' + stream.label() + ']"')
                        self._command.append('handler="[' + stream.label() + ']"')
                    self._command.append("-disposition:v:" + str(video_count))
                    self._command.append(str(deposition))
                    video_count += 1
                elif stream.stream_type() == "audio":
                    if stream.label() != "":
                        self._command.append("-metadata:a:" + str(audio_count))
                        self._command.append('title="[' + stream.label() + ']"')
                        self._command.append('handler="[' + stream.label() + ']"')
                    self._command.append("-disposition:a:" + str(audio_count))
                    self._command.append(str(deposition))
                    audio_count += 1
                elif stream.stream_type() == "subtitle":
                    if stream.label() != "":
                        self._command.append("-metadata:s:" + str(subtitle_count))
                        self._command.append('title="[' + stream.label() + ']"')
                        self._command.append('handler="[' + stream.label() + ']"')
                    self._command.append("-disposition:s:" + str(subtitle_count))
                    self._command.append(str(deposition))
                    subtitle_count += 1

        #video is HDR stuff bellow
        #https://forum.doom9.org/showthread.php?t=175227
        # https://trac.ffmpeg.org/ticket/5831
        #-pix_fmt yuv420p10le
        # -vf scale=out_color_matrix=bt2020:out_h_chr_pos=0:out_v_chr_pos=0,format=yuv420p10
        # # -c:v libx265 -preset medium
        # -x265-params :colorprim=bt2020:transfer=smpte-st-2048:colormatrix=bt2020nc:master-display=
        # "G(13250,34500)B(7500,3000)R(34000,16000)WP(15635,16450)L(12000000,200)":max-cll=
        # 0,0:repeat-headers
        # -c:a copy -max_muxing_queue_size 4096 "Sample_HDR-encode.mkv"

        # self.check_hdr(section_info.get("color_space", ""),
        #             section_info.get("color_transfer", ""),
        #             section_info.get("color_primaries", ""))
        # def check_hdr(self, space, transfer, primaries):
        #     '''checks and sets the HDR option'''
        #     if "bt2020" in space and transfer == "smpte2084" and primaries == "bt2020":
        #         self._hdr = True
        #         self._hdr_lock = True
        
        
        #check the video codes setting, figure out what is best default settings and set them for
        # x264 and x265 then extend the options for the custom versions with all the settings and
        # then in here make the command from them do it in another method
        #Deal with video resolution here
        config_video_max_height = self._conf["videoresolution"]
        video_info = self._probe_info.get_video_info()
        video_height = video_info[0]['height']
        if config_video_max_height != "keep":
            if config_video_max_height == "sd": #576 or 480
                if video_height > 576: # PAL spec resolution
                    self._command.append("-vf")
                    self._command.append("scale=-2:480")
            else: # HD videos Here
                if video_height > config_video_max_height:
                    self._command.append("-vf")
                    self._command.append("scale=-2:" + config_video_max_height)

        #Deal with video codec here
        #https://en.wikibooks.org/wiki/Category:Book:FFMPEG_An_Intermediate_Guide
        #https://github.com/senko/python-video-converter/ <-- use as a starting point
        #https://ffmpeg.org/ffmpeg.html
        #https://ffmpeg.org/pipermail/ffmpeg-user/2016-August/033183.html
        #how to detect HDR https://video.stackexchange.com/questions/22059/how-to-identify-hdr-video
        #https://github.com/ruediger/VobSub2SRT

        #tell ffmpeg to copy the audio
        self._command.append('-c:a')
        self._command.append('copy')

        #tell ffmpeg to copy the subtitles
        self._command.append('-c:s')
        self._command.append('copy')

        #tell ffmpag the output file
        self._command.append('"' + self._outfile + '"')
        return True


    def _map_stream(self, index, stream):
        '''system to return if to map the stream'''
        stream_info = self._probe_info.get_stream(index)
        stream_language = stream_info.get("tags", {}).get("language", "eng")
        stream_format = stream_info.get("codec_name", "")
        if stream.stream_type() == "video":
            return True
        elif stream.stream_type() == "audio":
            if stream.duplicate():
                return False
            if self._conf["audiolanguage"] == "all":
                if self._conf["audioformat"] == "all":
                    return True
                elif self._conf["audioformat"] == "highest":
                    #TODO work out how to detect this
                    pass
                elif self._conf["audioformat"] == "selected":
                    if stream_format in self._conf['audioformats']:
                        return True
            elif self._conf["audiolanguage"] == "original":
                if stream_language == self._disc_language:
                    if self._conf["audioformat"] == "all":
                        return True
                    elif self._conf["audioformat"] == "highest":
                        #TODO work out how to detect this
                        pass
                    elif self._conf["audioformat"] == "selected":
                        if stream_format in self._conf['audioformats']:
                            return True
            elif self._conf["audiolanguage"] == "selectedandoriginal":
                original_bool = stream_language == self._disc_language
                selected_bool = stream_language in self._conf['audiolanguages']
                if original_bool or selected_bool:
                    if self._conf["audioformat"] == "all":
                        return True
                    elif self._conf["audioformat"] == "highest":
                        #TODO work out how to detect this
                        pass
                    elif self._conf["audioformat"] == "selected":
                        if stream_format in self._conf['audioformats']:
                            return True
            elif self._conf["audiolanguage"] == "selected":
                if stream_language in self._conf['audiolanguages']:
                    if self._conf["audioformat"] == "all":
                        return True
                    elif self._conf["audioformat"] == "highest":
                        #TODO work out how to detect this
                        pass
                    elif self._conf["audioformat"] == "selected":
                        if stream_format in self._conf['audioformats']:
                            return True
        elif stream.stream_type() == "subtitle":
            if stream.duplicate():
                return False
            if stream.hearing_impaired() is True:
                if self._conf['keepclosedcaptions']:
                    if self._conf["subtitle"] == "all":
                        return True
                    elif self._conf["subtitle"] == "selected":
                        if stream_language in self._conf['subtitlelanguages']:
                            return True
            elif stream.comment() is True:
                if self._conf['keepcommentary']:
                    if self._conf["subtitle"] == "all":
                        return True
                    elif self._conf["subtitle"] == "selected":
                        if stream_language in self._conf['subtitlelanguages']:
                            return True
            else:
                if self._conf["subtitle"] == "all":
                    return True
                elif self._conf["subtitle"] == "selected":
                    if stream_language in self._conf['subtitlelanguages']:
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


    def _do_conversion(self, command):
        '''method to convert file'''
        pass

        # os.rename(infile, infile + ".OLD")
        # os.rename(outfile, infile)
        # os.remove(infile + ".OLD")
        # self._db.update(self._thread_name,
        #                 CONVERT_DB["name"],
        #                 self._sql_row_id, {"converted":True})
