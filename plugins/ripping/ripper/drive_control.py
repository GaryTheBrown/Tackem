'''CD/DVD/BLURAY Drive Controller (Currently Linux only)'''
from subprocess import Popen, PIPE, DEVNULL
import os
import shlex
import time
import threading



class DriveOLD:
    '''Drive Control ripper program self contained'''

##########
##CHECKS##
##########

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
