'''Master Section for the Converter controller'''
import threading
import os
import os.path
import time
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from .data.db_tables import VIDEO_CONVERT_DB_INFO as CONVERT_DB
from .ffprobe import FFprobe

class ConverterThread():
    '''Master Section for the Converter controller'''
    def __init__(self, item, config, db, tasks_sema):
        self._id = item['id']
        self._filename = item['filename']
        self._disc_info = item['disc_info']
        self._track_info = item['track_info']
        self._config = config
        self._db = db
        self._tasks_sema = tasks_sema
        self._thread = threading.Thread(target=self.run, args=())
        self._thread_name = "Converter Task " + str(self._id)
        self._thread.setName(self._thread_name)
        self._thread_run = False
        self._task_done = False
        self._sql_row_id = self._db.table_has_row(self._thread_name,
                                                  CONVERT_DB["name"],
                                                  {"id":self._id})

    def task_done(self):
        '''returns if the task is done'''
        return self._task_done

##########
##Thread##
##########
    def start_thread(self):
        '''start the thread'''
        self._thread.start()
        self._thread_run = True

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
            return
        command = self._create_command()
        if command is None:
            self._thread_run = False
        if not self._thread_run:
            return
        print("CONVERTER", self._id, ":COMMAND:", command)
        #run converter here with above command
        time.sleep(5.0)
        self._task_done = True
        self._tasks_sema.release()

    def _create_command(self):
        '''creates the conversion command here'''
                #actions here
        temp_location = self._config['locations']['videoripping']
        if temp_location[0] != "/":
            temp_location = PROGRAMCONFIGLOCATION + self._config['locations']['videoripping']
        infile = temp_location + self._filename
        outfile = temp_location + self._filename + ".NEW.mkv"
        if not os.path.exists(infile):
            print("ERROR:" + infile + " missing")
            return None# PROBLEM HERE AS IN FILE MISSING
        if os.path.exists(outfile):
            os.remove(outfile)

        con_config = self._config['converter']
        probe_info = FFprobe(con_config['ffprobelocation'], self._filename)

        command = []
        command.append(con_config['ffmpeglocation']) # ffmpeg program
        command.append("-i")
        command.append('"' + self._filename + '"')

        if con_config['videoinserttags']:
            #Deal with tagging here
            #https://kodi.wiki/view/Video_file_tagging#Title
            # “title”
            # “description”
            # “language”

            #-metadata title="Track #5" 
            pass

        #Deal with chapters here
        if probe_info.has_chapters():
            command.append("-map_chapters")
            if con_config['keepchapters']:
                command.append("0")
            else:
                command.append("-1")

        #video is HDR stuff bellow
        #https://forum.doom9.org/showthread.php?t=175227
        #-pix_fmt yuv420p10le
        # -vf scale=out_color_matrix=bt2020:out_h_chr_pos=0:out_v_chr_pos=0,format=yuv420p10
        # -c:v libx265 -preset medium
        # -x265-params :colorprim=bt2020:transfer=smpte-st-2048:colormatrix=bt2020nc:master-display=
        # "G(13250,34500)B(7500,3000)R(34000,16000)WP(15635,16450)L(12000000,200)":max-cll=
        # 0,0:repeat-headers
        # -c:a copy -max_muxing_queue_size 4096 "Sample_HDR-encode.mkv"

        #Deal with video resolution here
        # config_video_max_height = con_config["videoresolution"]
        # video_info = probe_info.get_video_info()
        # video_height = video_info[0]['height']
        # if config_video_max_height != "keep":
        #     if config_video_max_height == "sd": #576 or 480
        #         if video_height > 576: # PAL spec resolution
        #             command.append("-vf")
        #             command.append("scale=-2:480")
        #     else: # HD videos Here
        #         if video_height > config_video_max_height:
        #             command.append("-vf")
        #             command.append("scale=-2:" + config_video_max_height)

        #Deal with video codec here

        #Deal with audio here
        # audio_info = probe_info.get_audio_info()
        # audio_tracks_to_keep = []
        # audio_tracks_to_remove = []
        # commentary_tracks = []
        # commentary_track = self._track_data.commentary_track()
        # if commentary_track:
        #     if isinstance(commentary_track, int):
        #         for count, stream in enumerate(audio_info):
        #             if stream['index'] == commentary_track:
        #                 if con_config['keepcommentary']:
        #                     commentary_tracks.append(count)
        #                     audio_tracks_to_keep.append(count)
        #                 else:
        #                     audio_tracks_to_remove.append(count)
        #                 break
        #     elif isinstance(commentary_track, list):
        #         for count, stream in enumerate(audio_info):
        #             if stream['index'] in commentary_track:
        #                 if con_config['keepcommentary']:
        #                     commentary_tracks.append(count)
        #                     audio_tracks_to_keep.append(count)
        #                 else:
        #                     audio_tracks_to_remove.append(count)
        #                 break
        #     #visual_impaired
        # if con_config["audiolanguage"] == "all" and con_config["audiolanguage"] == "all":
        #     pass


        #create audio map list here with disposition info where needed matching new track numbering
        # command.append("-disposition:a:" + count)
        # command.append("comment")
        #Deal with subtitles here
        #forced & hearing_impared(closed captions)

        #https://github.com/senko/python-video-converter/ <-- use as a starting point
        #https://ffmpeg.org/ffmpeg.html
        # ffmpeg -i "infile" -map 0:v? -map 0:a? -map 0:s? "outfile"
        #metadata title changed by data passed in.
        #subtitle disposition for closed captions using subtitle format due to makemkv converting
        #still need to figure out how to do diposition for commentary
        #forign languages audio and subtitles set to dubbed
        # them to subrip to hearing_impared
        #https://ffmpeg.org/pipermail/ffmpeg-user/2016-August/033183.html
        #then work through each stream and copy or drop depending on settings
        #how to detect HDR https://video.stackexchange.com/questions/22059/how-to-identify-hdr-video
        return command

    def _do_conversion(self, command):
        '''method to convert file'''
        pass

        # os.rename(infile, infile + ".OLD")
        # os.rename(outfile, infile)
        # os.remove(infile + ".OLD")
        # self._db.update(self._thread_name,
        #                 CONVERT_DB["name"],
        #                 self._sql_row_id, {"converted":True})
