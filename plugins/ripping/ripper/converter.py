'''Master Section for the Converter controller'''
import threading
import time
from .data.db_tables import VIDEO_CONVERT_DB_INFO as CONVERT_DB
from .converter_thread import ConverterThread
from .data.events import RipperEvents

class Converter():
    '''Master Section for the Converter controller'''
    def __init__(self, config, db):
        self._config = config
        self._db = db
        self._thread_name = "Converter"
        self._thread = threading.Thread(target=self.run, args=())
        self._thread.setName(self._thread_name)
        self._thread_run = True

        self._max_thread_count = self._config['converter']['threadcount']
        self._thread_count = 0

        self._tasks_sema = threading.Semaphore(self._max_thread_count)
        self._tasks = []

##########
##Thread##
##########

    def start_thread(self):
        '''start the thread'''
        if not self._thread.is_alive():
            self._thread.start()
            return True
        return False

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
        while self._thread_run:
            check = {"converted":False}
            return_data = self._db.select(self._thread_name, CONVERT_DB["name"], check)
            data = []
            if return_data:
                if isinstance(return_data[0], list):
                    data = return_data[0]
                elif isinstance(return_data[0], dict):
                    data.append(return_data[0])
                for item in data:
                    self._tasks.append(ConverterThread(item['id'], item['disc_uuid'],
                                                       item['filename'], item['disc_info'],
                                                       item['rip_data'], self._config, self._db,
                                                       self._tasks_sema))
                for task in self._tasks:
                    task.start_thread()

                while self._tasks:
                    time.sleep(5.0)
                    i = 0
                    count = len(self._tasks)
                    while i < count:
                        if self._tasks[i].task_done():
                            del self._tasks[i]
                            count -= 1
                        else:
                            i += 1

            if not self._thread_run:
                return
            RipperEvents().converter.clear()
            RipperEvents().converter.wait()
            time.sleep(1.0)

def create_converter_row(sql, thread_name, uuid, label, disc_rip_info, to_rip):
    '''Function to add tracks to Convertor DB'''
    track_name = label + "/" + "t"
    for i, track in enumerate(disc_rip_info.tracks()):
        if track.video_type() in to_rip:
            file_name = track_name + str(i).zfill(2) + ".mkv"
            to_save = {
                "disc_uuid":uuid,
                "filename":file_name,
                "disc_info":disc_rip_info.make_dict(no_tracks=True),
                "rip_data":track.__dict__
            }
            sql.insert(thread_name, CONVERT_DB["name"], to_save)
