'''CD/DVD/BLURAY Drive Controller (Currently Linux only)'''
from subprocess import Popen, PIPE, DEVNULL
import os
import shlex
import time
import threading
import json
from libs.sql.column import Column

class Drive:
    '''Drive Control ripper program self contained'''

    _drive_lock = threading.Lock()
    _tray_open = False
    _tray_open_lock = threading.Lock()
    _tray_locked = False
    _tray_locked_lock = threading.Lock()
    _disc_in_drive = False
    _disc_in_drive_lock = threading.Lock()
    _drive_locked = False
    _drive_locked_lock = threading.Lock()
    _disc_info = {}
    _disc_info_lock = threading.Lock()
    _disc_rip_info = False
    _disc_rip_info_lock = threading.Lock()
    _disc_is_cd = False
    _disc_is_cd_lock = threading.Lock()
    _disc_size = 0
    _disc_size_lock = threading.Lock()
    _thread_run = True

    _DB_DVD_BLURAY_TABLE_NAME = "ripper"
    _DB_DVD_BLURAY_TABLE_DATA = [
        Column("id", "integer", primary_key=True, not_null=True),
        Column("uuid", "varchar(16)", not_null=True),
        Column("label", "text", not_null=True),
        Column("makemkv_info", "json"),
        Column("rip_data", "json"),
    ]
    _DB_DVD_BLURAY_TABLE_VERSION = 1

    def __init__(self, device, db):
        '''Setup Drive for Use'''
        self._device = device
        self._db = db

        self._thread = threading.Thread(target=self.run, args=())
        self._thread.setName("Ripper:" + self._device)

        db.table_check(self._thread.getName(),
                       self._DB_DVD_BLURAY_TABLE_NAME,
                       self._DB_DVD_BLURAY_TABLE_DATA,
                       self._DB_DVD_BLURAY_TABLE_VERSION)

###########
##SETTERS##
###########
    def _set_tray_open(self, value):
        '''Threadded Safe Set tray open'''
        with self._tray_open_lock:
            self._tray_open = bool(value)

    def _set_tray_locked(self, value):
        '''Threadded Safe Set tray locked'''
        with self._tray_locked_lock:
            self._tray_locked = bool(value)

    def _set_disc_in_drive(self, value):
        '''Threadded Safe Set disc in drive'''
        with self._disc_in_drive_lock:
            self._disc_in_drive = bool(value)


    def _set_drive_locked(self, value):
        '''Threadded Safe Set drive locked'''
        with self._drive_locked_lock:
            self._drive_locked = bool(value)

    def _set_disc_info(self, value):
        '''Threadded Safe Set disc info'''
        with self._disc_info_lock:
            self._disc_info = value

    def _set_disc_size(self, value):
        '''Threadded Safe Set disc size'''
        with self._disc_size_lock:
            self._disc_size = int(value)

    def _set_disc_is_cd(self, value):
        '''Threadded Safe Set disc is cd'''
        with self._disc_is_cd_lock:
            self._disc_is_cd = bool(value)

    def _set_disc_rip_info(self, value):
        '''Threadded Safe Set disc info'''
        with self._disc_rip_info_lock:
            self._disc_rip_info = value

    def _set_disc_info_key(self, key, value):
        '''Threadded Safe Set disc info'''
        with self._disc_info_lock:
            self._disc_info[key] = value


###########
##GETTERS##
###########
    def is_tray_open(self):
        '''returns if the tray is open'''
        with self._tray_open_lock:
            tray_open = self._tray_open
        return tray_open

    def is_tray_locked(self):
        '''returns if the tray is locked'''
        with self._tray_locked_lock:
            tray_locked = self._tray_locked
        return tray_locked

    def is_disc_in_drive(self):
        '''returns if a disc is in the drive'''
        with self._disc_in_drive_lock:
            disc_in_drive = self._disc_in_drive
        return disc_in_drive

    def is_drive_locked(self):
        '''returns if the drive is locked for another action'''
        with self._drive_locked_lock:
            drive_locked = self._drive_locked
        return drive_locked

    def is_disc_cd(self):
        '''returns if the disc is a cd'''
        if not self._tray_open and self._disc_in_drive:
            with self._disc_is_cd_lock:
                disc_is_cd = self._disc_is_cd
            return disc_is_cd
        return False

    def get_device(self):
        '''returns device device READ ONLY SO THREAD SAFE'''
        return self._device

    def get_disc_info(self):
        '''returns the disc UUID if a disc is in the drive'''
        if not self._tray_open and self._disc_in_drive:
            with self._disc_info_lock:
                disc_info = self._disc_info
            return disc_info
        return False

    def get_disc_label(self):
        '''returns the disc label if a disc is in the drive'''
        if not self._tray_open and self._disc_in_drive:
            with self._disc_info_lock:
                label = self._disc_info['Label']
            return label
        return False

    def get_disc_type(self):
        '''returns the disc type if a disc is in the drive'''
        if not self._tray_open and self._disc_in_drive:
            with self._disc_info_lock:
                disc_type = self._disc_info['Type']
            return disc_type
        return False

    def get_disc_size(self):
        '''returns the disc size if a disc is in the drive'''
        if not self._tray_open and self._disc_in_drive:
            with self._disc_size_lock:
                disc_size = self._disc_size
            return disc_size
        return False

    def get_disc_rip_info(self):
        '''returns the disc size if a disc is in the drive'''
        if not self._tray_open and self._disc_in_drive:
            with self._disc_rip_info_lock:
                disc_rip_info = self._disc_rip_info
            return disc_rip_info
        return False

    def get_thread_run(self):
        '''return if thread is running'''
        return self._thread.is_alive()

##########
##CHECKS##
##########
    def _check_if_tray_is_open(self):
        '''Will return if drive is closed or it will return a string of the error'''
        with self._drive_lock:
            cmd = [os.getcwd() + "/bin/TrayOpenCheck", self._device]
            process = Popen(cmd, stdout=PIPE, stderr=DEVNULL)
            process.communicate()
            exit_code = process.wait()

        if exit_code == 2:
            self._set_disc_in_drive(False)
            return False
        else:
            self._set_tray_open(exit_code)
            return bool(exit_code)

    def _check_disc_information(self):
        '''Will return if disc is in drive (setting the UUID and label) or it will return False'''
        with self._drive_lock:
            process = Popen(["blkid", self._device], stdout=PIPE, stderr=DEVNULL)
            returned_message = process.communicate()[0]
            process.wait()
        if not returned_message:
            self._set_disc_in_drive(False)
            return False
        self._set_disc_in_drive(True)
        message = shlex.split(returned_message.decode('ascii').rstrip().split(": ")[1])
        uuid = message[0].split("=")[1]
        self._disc_info_lock.acquire()
        self._disc_info['UUID'] = uuid
        self._disc_info['Label'] = message[1].split("=")[1]
        self._disc_info_lock.release()
        return True

    def _check_disc_size(self):
        '''Will return the size of the disc or false if no disc in the drive'''
        with self._drive_lock:
            process = Popen(["blockdev", "--getsize64", self._device], stdout=PIPE, stderr=DEVNULL)
            returned_message = process.communicate()[0]
            process.wait()
            message = returned_message.decode('ascii').rstrip()
        if "No medium found" in message or message == '':
            self._set_disc_in_drive(False)
            return False
        self._set_disc_in_drive(True)
        self._set_disc_size(message)
        return True

    def _check_audio_disc_information(self):
        '''Will return if drive is open or it will return a string of the error'''
        with self._drive_lock:
            process = Popen(["cdrdao", "discid", "--device", self._device],
                            stdout=PIPE, stderr=DEVNULL)
            returned_message = process.communicate()[0].decode('ascii').rstrip().split("\n")
            process.wait()
        if not returned_message:
            return False
        self._set_disc_in_drive(True)
        disc_rip_info = {}
        for line in returned_message:
            disc_rip_info[line.split(":")[0]] = line.split(":")[1]

        self._set_disc_rip_info(disc_rip_info)
        return True

################
##TRAYCONTROLS##
################
    def open_tray(self):
        '''Send Command to open the tray'''
        with self._drive_lock:
            self._set_drive_locked(True)
            Popen(["eject", self._device]).wait()
            self._set_tray_open(True)
            self._set_drive_locked(False)

    def close_tray(self):
        '''Send Command to close the tray'''
        with self._drive_lock:
            self._set_drive_locked(True)
            Popen(["eject", "-t", self._device]).wait()
            self._set_tray_open(False)
            self._set_drive_locked(False)

    def lock_tray(self):
        '''Send Command to lock the tray'''
        with self._drive_lock:
            self._set_drive_locked(True)
            Popen(["eject", "-i1", self._device]).wait()
            self._set_tray_locked(True)
            self._set_drive_locked(False)

    def unlock_tray(self):
        '''Send Command to unlock the tray'''
        with self._drive_lock:
            self._set_drive_locked(True)
            Popen(["eject", "-i0", self._device]).wait()
            self._set_tray_locked(False)
            self._set_drive_locked(False)

#########
##WAITS##
#########
    def _wait_for_user_close_tray(self, sleep_time=1.0, timeout=10):
        '''Waits for the Drive to close for when the user is to input a disc'''
        count = 0
        while self._check_if_tray_is_open():
            if count >= timeout:
                return False
            time.sleep(float(sleep_time))
            count += 1
        return True

    def _wait_for_user_open_tray(self, sleep_time=1.0, timeout=10):
        '''Waits for the Drive to close for when the user is to input a disc'''
        count = 0
        while not self._check_if_tray_is_open():
            if count >= timeout:
                return False
            time.sleep(float(sleep_time))
            count += 1
        return True

    def _wait_for_disc(self, sleep_time=1.0, timeout=10):
        '''waits for the disc info to be found'''
        count = 0
        while self.get_disc_size() == 0:
            if count >= timeout:
                return False
            self._check_disc_size()
            time.sleep(float(sleep_time))
            count += 1
        if self.get_disc_size() <= 912261120:
            self._set_disc_is_cd(True)
        return True


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
                                                self._DB_DVD_BLURAY_TABLE_NAME,
                                                check)

                row = {"uuid":self._disc_info['UUID'],
                       "label":self._disc_info['Label']}
                if 'makemkv_info' in self._disc_info:
                    row['makemkv_info'] = self._disc_info['makemkv_info']
                if self._disc_rip_info:
                    row['rip_data'] = self._disc_rip_info

                if row_id == 0:
                    self._db.insert(self._thread.getName(),
                                    self._DB_DVD_BLURAY_TABLE_NAME,
                                    row)
                else:
                    self._db.update(self._thread.getName(),
                                    self._DB_DVD_BLURAY_TABLE_NAME,
                                    row_id, row)

    def _check_and_return_from_db(self):
        '''check for disc in DB and return it's info if found'''
        with self._disc_info_lock:
            check = {"uuid":self._disc_info['UUID'],
                     "label":self._disc_info['Label']}
            return_data = None
            if self._db.table_has_row(self._thread.getName(),
                                      self._DB_DVD_BLURAY_TABLE_NAME,
                                      check):
                return_data = self._db.select(self._thread.getName(),
                                              self._DB_DVD_BLURAY_TABLE_NAME,
                                              check, ["rip_data"])
                with self._disc_rip_info_lock:
                    self._disc_rip_info = json.loads(return_data[0][0])
        if not return_data:
            return False
        return True

#############################
##EXTERNAL APPS THREAD SAFE##
#############################
    def call_makemkv_info(self):
        '''run the _ function Thread Safe'''
        with self._drive_lock:
            self._set_disc_info_key('Info', self._makemkv_info(self._device))

    def call_makemkv_backup(self):
        '''run the makemkv backup function thread safe'''
        temp_dir = "temp/" + self.get_disc_info()['Label'].replace(" ", "_")
        with self._drive_lock:
            if isinstance(self._disc_rip_info, list):
                for idx, track in enumerate(self._disc_rip_info):
                    if not isinstance(track, bool):
                        self._makemkv_backup(self._device, temp_dir, idx)
            elif isinstance(self._disc_rip_info, bool):
                self._makemkv_backup(self._device, temp_dir)

    def _makemkv_info(self, device):
        '''Get info from within makemkv'''
        #inital dictionary for return
        rdict = {}
        rdict['track_count'] = 0
        rdict['cinfo'] = {}
        rdict['Tracks'] = []


        values = [
            'unknown', 'Type', 'Name', 'LangCode', 'LangName', 'CodecId', 'CodecShort',
            'CodecLong', 'ChapterCount', 'Duration', 'DiskSize', 'DiskSizeBytes',
            'StreamTypeExtension', 'Bitrate', 'AudioChannelsCount', 'AngleInfo',
            'SourceFileName', 'AudioSampleRate', 'AudioSampleSize', 'VideoSize',
            'VideoAspectRatio', 'VideoFrameRate', 'StreamFlags', 'DateTime',
            'OriginalTitleId', 'SegmentsCount', 'SegmentsMap', 'OutputFileName',
            'MetadataLanguageCode', 'MetadataLanguageName', 'TreeInfo', 'PanelTitle',
            'VolumeName', 'OrderWeight', 'OutputFormat', 'OutputFormatDescription',
            'SeamlessInfo', 'PanelText', 'MkvFlags', 'MkvFlagsText', 'AudioChannelLayoutName',
            'OutputCodecShort', 'OutputConversionType', 'OutputAudioSampleRate',
            'OutputAudioSampleSize', 'OutputAudioChannelsCount', 'OutputAudioChannelLayoutName',
            'OutputAudioChannelLayout', 'OutputAudioMixDescription', 'Comment', 'OffsetSequenceId'
        ]

        prog_args = [
            "makemkvcon",
            "-r",
            "--messages=-stdout",
            "--progress=-null",
            "info",
            "dev:" + device
        ]
        process = Popen(prog_args, stdout=PIPE, stderr=DEVNULL)
        returned_message = process.communicate()[0].decode('ascii').split("\n")
        process.wait()
        try:
            os.remove("wget-log")
            os.remove("wget-log.1")
        except OSError:
            pass

        for line in returned_message:
            first_split_line = line.split(":", 1)
            if first_split_line[0] == "TCOUNT":
                rdict['track_count'] = int(line.split(":")[-1])
                rdict['Tracks'] = [dict() for x in range(rdict['track_count'])]
            elif first_split_line[0] == "CINFO":
                new_line = first_split_line[1].split(",", 2)
                id_value = int(new_line[0])
                value = new_line[2].replace('"', "").replace("<b>", "").replace("</b><br>", "")
                rdict[values[id_value]] = value
            elif first_split_line[0] == "Tracks":
                new_line = first_split_line[1].split(",", 3)
                track_id = int(new_line[0])
                id_value = int(new_line[1])
                value = new_line[3].replace('"', "").replace("<b>", "").replace("</b><br>", "")
                rdict['Tracks'][track_id][values[id_value]] = value
            elif first_split_line[0] == "SINFO":
                new_line = first_split_line[1].split(",", 4)
                track_id = int(new_line[0])
                track_sub_id = int(new_line[1])
                id_value = int(new_line[2])
                value = new_line[4].replace('"', "").replace("<b>", "").replace("</b><br>", "")
                #setup sinfo if not already there
                if not "sinfo" in  rdict['Tracks'][track_id]:
                    rdict['Tracks'][track_id]['sinfo'] = []
                #Get sub array size matching for current number
                while len(rdict['Tracks'][track_id]['sinfo']) <= track_sub_id:
                    tempdict = {}
                    rdict['Tracks'][track_id]['sinfo'].append(tempdict)
                rdict['Tracks'][track_id]['sinfo'][track_sub_id][values[id_value]] = value
        return rdict

    def _makemkv_backup(self, device, temp_dir, index=-1):
        '''Do the mkv Backup still needs to be converted to prefered codec'''
        try:
            os.mkdir(temp_dir)
        except OSError:
            pass

        if index == -1:
            index = "all"

        prog_args = [
            "makemkvcon",
            "-r",
            "--messages=-null",
            "--progress=-stdout",
            "mkv",
            "dev:" + device,
            str(index),
            temp_dir
        ]
        process = Popen(prog_args, stdout=DEVNULL, stderr=DEVNULL)
        process.communicate()
        process.wait()
        try:
            os.remove("wget-log")
            os.remove("wget-log.1")
        except OSError:
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

##########
##Script##
##########
    def run(self):
        ''' Loops through the standard ripper function'''
        while self._thread_run:
            #This Section will make the thread wait for a
            #disc before continuing but will exit whenever it is asked to
            if not self._wait_for_disc(timeout=15):
                while not self._wait_for_user_open_tray(timeout=2):
                    if not self._thread_run:
                        return
                while not self._wait_for_user_close_tray(timeout=2):
                    if not self._thread_run:
                        return
                continue
            if self.is_disc_cd():
                self._check_audio_disc_information()
                #TODO AUDIO CD RIPPING HERE
            else:
                self._check_disc_information()
                if not self._check_and_return_from_db():
                    if not self._check_disc_id():
                        makemkv_info_temp = self._makemkv_info(self._device)
                        with self._disc_info_lock:
                            self._disc_info['makemkv_info'] = makemkv_info_temp
                    self._save_to_db()

            #END OF LOOP
            self.open_tray()
            time.sleep(10)
            while not self._wait_for_user_close_tray():
                if not self._thread_run:
                    return
