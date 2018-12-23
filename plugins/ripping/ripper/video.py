'''video ripping controller'''
from abc import ABCMeta, abstractmethod
import threading
import json
from libs.sql.column import Column

VIDEO_DB_INFO = {
    "name": "ripper_video_info",
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

class Video(metaclass=ABCMeta):
    '''video ripping controller'''
    def __init__(self, device, config, db, thread_name):
        self._device = device
        self._config = config
        self._db = db
        self._thread_name = thread_name
        self._disc_info_lock = threading.Lock()
        self._disc_info_uuid = None
        self._disc_info_label = None
        self._makemkv_info_lock = threading.Lock()
        self._makemkv_info = None
        self._disc_rip_info_lock = threading.Lock()
        self._disc_rip_info = None
###########
##SETTERS##
###########
    def _set_disc_info(self, uuid, label):
        '''Threadded Safe Set disc info'''
        with self._disc_info_lock:
            self._disc_info_uuid = uuid
            self._disc_info_label = label

    def _set_makemkv_info(self, makemkv_info):
        '''Threadded Safe Set makemkv info'''
        with self._makemkv_info_lock:
            self._makemkv_info = makemkv_info

    def _set_disc_rip_info(self, disc_rip_info):
        '''Threadded Safe Set disc_rip info'''
        with self._disc_rip_info_lock:
            self._disc_rip_info = disc_rip_info
###########
##GETTERS##
###########
    def get_disc_info_uuid(self):
        '''returns the disc UUID'''
        with self._disc_info_lock:
            uuid = self._disc_info_uuid
        return uuid

    def get_disc_info_label(self):
        '''returns the disc label'''
        with self._disc_info_lock:
            label = self._disc_info_label
        return label

    def get_makemkv_info(self):
        '''returns the mekemkv info'''
        with self._makemkv_info_lock:
            makemkv_info = self._makemkv_info
        return makemkv_info

    def get_disc_rip_info(self):
        '''returns the disc rip info'''
        with self._disc_rip_info_lock:
            disc_rip_info = self._disc_rip_info
        return disc_rip_info

##########
##CHECKS##
##########
    @abstractmethod
    def _check_disc_information(self):
        '''Will set the UUID and label or it will return False'''
        pass

###################
##MAKEMKV CALLERS##
###################
    def _call_makemkv_info(self):
        '''run the _ function Thread Safe'''
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
        returned_message = self._makemkv_info_from_disc()
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
            self._set_makemkv_info(rdict)

    def call_makemkv_backup(self):
        '''run the makemkv backup function thread safe'''
        temp_dir = "temp/" + self.get_disc_info_label()
        if isinstance(self._disc_rip_info, list):
            for idx, track in enumerate(self._disc_rip_info):
                if not isinstance(track, bool):
                    self._makemkv_backup_from_disc(temp_dir, idx)
        elif isinstance(self._disc_rip_info, bool):
            self._makemkv_backup_from_disc(temp_dir)

    @abstractmethod
    def _makemkv_info_from_disc(self):
        '''Get info from within makemkv from disc'''
        pass

    @abstractmethod
    def _makemkv_backup_from_disc(self, temp_dir, index=-1):
        '''Do the mkv Backup from disc'''
        pass

#############
##API CALLS##
#############
    def _check_disc_id_on_api(self):
        ''' call the API function in a thread safe way when getting info needed'''
        uuid = self.get_disc_info_uuid()
        label = self.get_disc_info_label()
        rip_list = None#self._apiaccess_video_disc_id(uuid, label)
        if rip_list:
            self._set_disc_rip_info(rip_list)
            return True
        return False

    def _apiaccess_video_disc_id(self, uuid, label):
        '''will access the api and check if the disc exists
        TEMP FUNCTION BELLOW TO EXPAND WHEN READY TO.'''
        uuid_temp = "36cc8c4d00000000"
        label_temp = "AQUA_TEEN_COLON_MOVIE"
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
    def _save_to_video_db(self):
        '''Function to save data to DB'''
        info = {"uuid":self.get_disc_info_uuid(),
                "label":self.get_disc_info_label()}
        row_id = self._db.table_has_row(self._thread_name,
                                        VIDEO_DB_INFO["name"],
                                        info)
        makemkv_info = self.get_makemkv_info()
        if makemkv_info:
            info['makemkv_info'] = makemkv_info
        disc_rip_info = self.get_disc_rip_info()
        if self._disc_rip_info:
            info['rip_data'] = disc_rip_info

        if row_id == 0:
            self._db.insert(self._thread_name,
                            VIDEO_DB_INFO["name"],
                            info)
        else:
            #info in table so compare if different report this as Should never be
            self._db.update(self._thread_name,
                            VIDEO_DB_INFO["name"],
                            row_id, info)

    def _check_and_return_from_video_db(self):
        '''check for disc in DB and return it's info if found'''
        check = {"uuid":self.get_disc_info_uuid(),
                 "label":self.get_disc_info_label()}
        return_data = None
        if self._db.table_has_row(self._thread_name, VIDEO_DB_INFO["name"], check):
            return_data = self._db.select(self._thread_name, VIDEO_DB_INFO["name"],
                                          check, ["rip_data"])
            self._set_disc_rip_info(json.loads(return_data[0][0]))
        if not return_data:
            return False
        return True

##########
##Script##
##########
    def run(self):
        '''script to rip video disc'''
        self._check_disc_information()
        if not self._check_and_return_from_video_db():
            if not self._check_disc_id_on_api():
                self._call_makemkv_info()
                #need user input of disc ripping sections here
            self._save_to_video_db()

