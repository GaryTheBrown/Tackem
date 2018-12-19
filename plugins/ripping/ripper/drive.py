'''Master Section for the Drive controller'''
from abc import ABCMeta, abstractmethod
import threading
import time
import json
from libs.sql.column import Column

DB_INFO = {
    "DVDBLURAYINFOTABLE":
    {
        "name": "ripper_dvdbluray_info",
        "data":
            [
                Column("id", "integer", primary_key=True, not_null=True),
                Column("uuid", "varchar(16)", not_null=True),
                Column("label", "text", not_null=True),
                Column("makemkv_info", "json"),
                Column("rip_data", "json"),
            ],
        "version": 1
    }
}

class Drive(object, metaclass=ABCMeta):
    '''Master Section for the Drive controller'''

    def __init__(self, device_info, config, db):
        self._device_info = device_info
        self._device = device_info['link']
        self._config = config
        self._db = db

        self._thread = threading.Thread(target=self.run, args=())
        self._thread.setName("Ripper:" + self._device)

        self._thread_run = True
        self._drive_lock = threading.Lock()
        self._tray_status = self.check_tray()
        self._tray_status_lock = threading.Lock()
        self._tray_locked = False
        self._tray_locked_lock = threading.Lock()
        self._disc_size = 0
        self._disc_size_lock = threading.Lock()
        self._disc_info = {}
        self._disc_info_lock = threading.Lock()
        self._disc_rip_info = False
        self._disc_rip_info_lock = threading.Lock()

        for key in DB_INFO:
            self._db.table_check(self._thread.getName(),
                                 DB_INFO[key]["name"],
                                 DB_INFO[key]["data"],
                                 DB_INFO[key]["version"])

###########
##SETTERS##
###########
    def _set_tray_status(self, value):
        '''Threadded Safe Set tray open'''
        with self._tray_status_lock:
            self._tray_status = value

    def _set_tray_locked(self, value):
        '''Threadded Safe Set tray locked'''
        with self._tray_locked_lock:
            self._tray_locked = bool(value)

    def _set_disc_size(self, value):
        '''Threadded Safe Set disc size'''
        with self._disc_size_lock:
            self._disc_size = int(value)

    def _set_disc_info(self, value):
        '''Threadded Safe Set disc info'''
        with self._disc_info_lock:
            self._disc_info = value

    def _set_disc_info_key(self, key, value):
        '''Threadded Safe Set disc info'''
        with self._disc_info_lock:
            self._disc_info[key] = value

    def _set_disc_rip_info(self, value):
        '''Threadded Safe Set disc info'''
        with self._disc_rip_info_lock:
            self._disc_rip_info = value

###########
##GETTERS##
###########
    def get_device(self):
        '''returns device device READ ONLY SO THREAD SAFE'''
        return self._device

    def get_thread_run(self):
        '''return if thread is running'''
        return self._thread.is_alive()

    def get_tray_status(self):
        '''returns if the tray is open'''
        with self._tray_status_lock:
            tray_status = self._tray_status
        return tray_status

    def get_tray_locked(self):
        '''returns if the tray is locked'''
        with self._tray_locked_lock:
            tray_locked = self._tray_locked
        return tray_locked

    def get_disc_size(self):
        '''returns the disc size if a disc is in the drive'''
        if self.get_tray_status() == "loaded":
            with self._disc_size_lock:
                disc_size = self._disc_size
            return disc_size
        return False

    def get_is_disc_cd(self):
        '''returns if the disc is a cd'''
        if self.get_disc_size() <= 912261120:
            return True
        return False

    def get_disc_info(self):
        '''returns the disc UUID if a disc is in the drive'''
        if self.get_tray_status() == "loaded":
            with self._disc_info_lock:
                disc_info = self._disc_info
            return disc_info
        return False

    def get_disc_label(self):
        '''returns the disc label if a disc is in the drive'''
        if self.get_tray_status() == "loaded":
            with self._disc_info_lock:
                label = self._disc_info['Label']
            return label
        return False

    def get_disc_type(self):
        '''returns the disc type if a disc is in the drive'''
        if self.get_tray_status() == "loaded":
            with self._disc_info_lock:
                disc_type = self._disc_info['Type']
            return disc_type
        return False

##########
##CHECKS##
##########
    @abstractmethod
    def check_tray(self):
        '''check the status of the disc tray'''
        pass

    @abstractmethod
    def _check_disc_size(self):
        '''Will return the size of the disc or false if no disc in the drive'''
        pass

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


#############
##API CALLS##
#############
    def _check_disc_id(self):
        ''' call the API function in a thread safe way when getting info needed'''
        with self._disc_info_lock:
            uuid = self._disc_info['UUID']
            label = self._disc_info['Label']
        rip_list = self._apiaccess_video_disc_id(uuid, label)
        if rip_list:
            self._set_disc_rip_info(rip_list)
            return True
        return False

    def _apiaccess_video_disc_id(self, uuid, label):
        '''will access the api and check if the disc exists
        TEMP FUNCTION BELLOW TO EXPAND WHEN READY TO.'''
        uuid_temp = "36cc8c4d00000000"
        label_temp = "AQUA_TEEN_COLON_MOVIE"
        # print(uuid, label)
        # print(uuid_temp, label_temp)
        list_to_return = False

        if uuid == uuid_temp and label == label_temp:
            list_to_return = [
                {
                    'Type': "Movie",
                    'Name': "Aqua Teen Hunger Force Colon Movie",
                    "Year": "2007",
                    "imdb": "tt0455326",
                },
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False
            ]

        return list_to_return

############
##DATABASE##
############
    def _save_to_db(self):
        '''Function to save data to DB'''
        with self._disc_info_lock:
            with self._disc_rip_info_lock:
                check = {"uuid":self._disc_info['UUID'],
                         "label":self._disc_info['Label']}
                row_id = self._db.table_has_row(self._thread.getName(),
                                                DB_INFO["DVDBLURAYTABLE"]["NAME"],
                                                check)

                row = {"uuid":self._disc_info['UUID'],
                       "label":self._disc_info['Label']}
                if 'makemkv_info' in self._disc_info:
                    row['makemkv_info'] = self._disc_info['makemkv_info']
                if self._disc_rip_info:
                    row['rip_data'] = self._disc_rip_info

                if row_id == 0:
                    self._db.insert(self._thread.getName(),
                                    DB_INFO["DVDBLURAYTABLE"]["NAME"],
                                    row)
                else:
                    self._db.update(self._thread.getName(),
                                    DB_INFO["DVDBLURAYTABLE"]["NAME"],
                                    row_id, row)

    def _check_and_return_from_db(self):
        '''check for disc in DB and return it's info if found'''
        with self._disc_info_lock:
            check = {"uuid":self._disc_info['UUID'],
                     "label":self._disc_info['Label']}
            return_data = None
            if self._db.table_has_row(self._thread.getName(),
                                      DB_INFO["DVDBLURAYTABLE"]["NAME"],
                                      check):
                return_data = self._db.select(self._thread.getName(),
                                              DB_INFO["DVDBLURAYTABLE"]["NAME"],
                                              check, ["rip_data"])
                with self._disc_rip_info_lock:
                    self._disc_rip_info = json.loads(return_data[0][0])
        if not return_data:
            return False
        return True

#######
#WAITS#
#######
    def _wait_for_disc(self, sleep_time=1.0, timeout=10):
        '''waits for the disc info to be found'''
        count = 0
        while self.get_tray_status() != "loaded":
            if count >= timeout:
                return False
            time.sleep(float(sleep_time))
            count += 1
        self._check_disc_size()
        return True

##########
##Script##
##########
    def run(self):
        ''' Loops through the standard ripper function'''
        while self._thread_run:
            if not self._wait_for_disc(timeout=15):
                if not self._thread_run:
                    return
                continue
