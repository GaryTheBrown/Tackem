'''Master Section for the Video Converter controller'''
from abc import ABCMeta, abstractmethod
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

class VideoConverterBase(metaclass=ABCMeta):
    '''Master Section for the Video Converter controller'''

    def __init__(self, pool_sema: BoundedSemaphore, db_id: int):
        self.__thread = threading.Thread(target=self.run, args=())
        self.__thread.setName(f"Converter Task: {str(db_id)}")

        self.__pool_sema = pool_sema
        self.__db_id = db_id

        self.__conf = CONFIG['ripper']['converter']
        self.__filename = ""
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

    def api_data(self) -> dict:
        '''returns the data as dict for html'''
        file_name_split = self.__filename.replace(".mkv", "").split("/")
        return_dict = {
            'id': self._db_id,
            'discid': int(file_name_split[0]),
            'trackid': int(file_name_split[1]),
            'converting': self.__active,
            'count': self.__frame_count,
            'process': self.__frame_process,
            'percent': self.__percent
        }
        return return_dict

    def converting(self):
        '''return if converting'''
        return self.__active

    @abstractmethod
    def run(self):
        ''' Loops through the standard converter function'''

    @abstractmethod
    def _create_command(self):
        '''creates the conversion command here'''

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
