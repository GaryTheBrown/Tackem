'''Master Section for the Converter controller'''
import threading
import os
import os.path
import pexpect
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.scraper.scraper_base import Scraper
from libs.data.languages import Languages
from .data.db_tables import VIDEO_CONVERT_DB_INFO as CONVERT_DB
from .ffprobe import FFprobe
from .presets import get_video_preset_command

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
        self._outfile = self._infile.replace(".mkv", "") + ".NEW.mkv"
        self._disc_language = Languages().convert_2_to_3t(self._disc_info.language())
        self._conf = self._config['converter']
        self._probe_info = FFprobe(self._conf['ffprobelocation'], self._infile)
        self._command = []
        self._frame_count = None
        self._frame_process = 0
        self._percent = 0.0
        self._running = False

    def task_done(self):
        '''returns if the task is done'''
        return self._task_done

###########
##GETTERS##
###########

    def get_id(self):
        '''returns the ID'''
        return self._id

    def get_data(self):
        '''returns the data as dict for html'''
        file_name_split = self._filename.replace(".mkv", "").split("/")
        return_dict = {
            'id': self._id,
            'discid': int(file_name_split[0]),
            'trackid': int(file_name_split[1]),
            'converting': self._running,
            'count':self._frame_count,
            'process':self._frame_process,
            'percent':self._percent
        }
        return return_dict

    def converting(self):
        '''return if converting'''
        return self._running

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
        self._create_command()
        if not self._thread_run:
            self._tasks_sema.release()
            return
        self._get_frame_count()
        if self._do_conversion():
            os.rename(self._infile, self._infile + ".OLD")
            os.rename(self._outfile, self._infile)
            if not self._conf['keeporiginalfile']:
                os.remove(self._infile + ".OLD")
            self._db.update(self._thread_name,
                            CONVERT_DB["name"],
                            self._sql_row_id, {"converted":True})
        self._task_done = True
        self._tasks_sema.release()

    def _create_command(self):
        '''creates the conversion command here'''
        if not os.path.exists(self._infile):
            print("ERROR:" + self._infile + " missing")
            return False# PROBLEM HERE AS IN FILE MISSING
        if os.path.exists(self._outfile):
            os.remove(self._outfile)

        self._command.append(self._conf['ffmpeglocation'])
        self._command.append("-i")
        self._command.append('"' + self._infile + '"')

        #Deal with tagging here
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

        #Add metadata and dispositions for each track here
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
                        self._command.append("-metadata:s:v:" + str(video_count))
                        self._command.append('title="[' + stream.label() + ']"')
                        # self._command.append('handler="[' + stream.label() + ']"')
                    self._command.append("-disposition:v:" + str(video_count))
                    self._command.append(str(deposition))
                    video_count += 1
                elif stream.stream_type() == "audio":
                    if stream.label() != "":
                        self._command.append("-metadata:s:a:" + str(audio_count))
                        self._command.append('title="[' + stream.label() + ']"')
                        # self._command.append('handler="[' + stream.label() + ']"')
                    self._command.append("-disposition:a:" + str(audio_count))
                    self._command.append(str(deposition))
                    audio_count += 1
                elif stream.stream_type() == "subtitle":
                    if stream.label() != "":
                        self._command.append("-metadata:s:s:" + str(subtitle_count))
                        self._command.append('title="[' + stream.label() + ']"')
                        # self._command.append('handler="[' + stream.label() + ']"')
                    self._command.append("-disposition:s:" + str(subtitle_count))
                    self._command.append(str(deposition))
                    subtitle_count += 1

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
        if self._conf['videocodec'] == "keep":
            self._command.append('-c:v')
            self._command.append('copy')
        elif self._conf['videocodec'] == "x264default":
            self._command.append('-c:v')
            self._command.append('libx264')
        elif self._conf['videocodec'] == "x265default":
            self._command.append('-c:v')
            self._command.append('libx265')
        elif self._conf['videocodec'] == "x264custom":
            self._command.append('-c:v')
            self._command.append('libx264')
            self._command.append('-preset')
            self._command.append(self._conf['x26preset'])
            self._command.append('-crf')
            if "10le" in video_info[0].get("pix_fmt", ""):
                self._command.append(str(self._conf['x26crf10bit']))
            else:
                self._command.append(str(self._conf['x26crf8bit']))
            if self._conf['x26extra']:
                self._command.append(str(self._conf['x26extra']))
        elif self._conf['videocodec'] == "x265custom":
            self._command.append('-c:v')
            self._command.append('libx265')
            self._command.append('-preset')
            self._command.append(self._conf['x26preset'])
            self._command.append('-crf')
            if "10le" in video_info[0].get("pix_fmt", ""):
                self._command.append(str(self._conf['x26crf10bit']))
            else:
                self._command.append(str(self._conf['x26crf8bit']))
            if self._conf['x26extra']:
                self._command.append(str(self._conf['x26extra']))
        elif self._conf['videocodec'] == "preset":
            video_command = get_video_preset_command(self._conf['videopreset'])
            self._command.append(video_command)

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

    def _get_frame_count(self):
        '''gets the frame count of the file'''
        cmd = 'ffmpeg -hide_banner -v quiet -stats -i "'
        cmd += self._infile
        cmd += '" -map 0:v:0 -c copy -f null -'
        frames = 0
        thread = pexpect.spawn(cmd, encoding='utf-8')
        cpl = thread.compile_pattern_list([pexpect.EOF, "frame= *\d+"])
        while True:
            i = thread.expect_list(cpl, timeout=None)
            if i == 0: # EOF
                break
            elif i == 1:
                frames = thread.match.group(0)
        self._frame_count = int(frames.replace("frame=", "").strip())

    def _do_conversion(self):
        '''method to convert file'''
        self._running = True
        thread = pexpect.spawn(" ".join(self._command), encoding='utf-8')
        cpl = thread.compile_pattern_list([pexpect.EOF, "frame= *\d+"])
        while True:
            i = thread.expect_list(cpl, timeout=None)
            if i == 0: # EOF
                self._running = False
                return True
            elif i == 1:
                return_string = thread.match.group(0).replace("frame=", "").lstrip()
                self._frame_process = int(return_string)
                self._percent = round(float(self._frame_process/ self._frame_count * 100), 2)
