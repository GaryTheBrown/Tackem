'''Master Section for the Video Converter controller'''
from threading import BoundedSemaphore
import threading
import pexpect
from data.config import CONFIG


class VideoConverterBase():
    '''Master Section for the Video Converter controller'''

    def __init__(self, pool_sema: BoundedSemaphore, db_id: int):
        self.__thread = threading.Thread(target=self.run, args=())
        self.__thread.setName(f"Converter Task: {str(db_id)}")

        self._pool_sema = pool_sema
        self._db_id = db_id

        self._conf = CONFIG['ripper']['converter']
        self._filename = ""
        self._command: list = []
        self.__frame_count: int = 0
        self.__frame_process: int = 0
        self.__percent: float = 0.0

        self._thread_run: bool = True
        self.__active: bool = False
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
            self._thread_run = False
            self.__thread.join()

    def api_data(self) -> dict:
        '''returns the data as dict for html'''
        file_name_split = self._filename.replace(".mkv", "").split("/")
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

    def _get_frame_count(self, infile: str):
        '''gets the frame count of the file'''
        cmd = 'ffmpeg -hide_banner -v quiet -stats -i "'
        cmd += infile
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
        self.__active = True
        thread = pexpect.spawn(" ".join(self._command), encoding='utf-8')
        cpl = thread.compile_pattern_list([pexpect.EOF, "frame= *\d+"])
        while True:
            i = thread.expect_list(cpl, timeout=None)
            if i == 0:  # EOF
                self.__active = False
                return True
            if i == 1:
                return_string = thread.match.group(
                    0).replace("frame=", "").lstrip()
                self.__frame_process = int(return_string)
                self.__percent = round(
                    float(self.__frame_process / self.__frame_count * 100), 2)
