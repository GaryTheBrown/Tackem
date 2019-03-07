'''Audio Ripping Feature'''
from abc import ABCMeta, abstractmethod
import discid
from .data.events import RipperEvents

#FORMATS - WAV OGG FLAC MP3 http://opus-codec.org/ http://www.wavpack.com/

#tagging data to be split between cd and track info for saving to the database for use later on
# when converting tag the files if possible at the same time otherwise convert then tag in the
# converter

class AudioCD(metaclass=ABCMeta):
    '''Audio ripping controller'''
    def __init__(self, device, config, db, thread_name, set_drive_status, thread_run):
        self._device = device
        self._events = RipperEvents()
        self._config = config
        self._db = db
        self._thread_name = thread_name
        self._thread_run = thread_run
        self._set_drive_status = set_drive_status
        self._disc_id = None
        self._db_id = None

        self._ripping_track = None
        self._ripping_file = 0
        self._ripping_total = 0
        self._ripping_max = 100
        self._ripping_file_p = 0.0
        self._ripping_total_p = 0.0
###########
##SETTERS##
###########

###########
##GETTERS##
###########

    def get_ripping_data(self):
        '''returns the data as dict for html'''
        return_dict = {
            'track':self._ripping_track,
            'file':self._ripping_file,
            'total':self._ripping_total,
            'max':self._ripping_max,
            'file_percent':self._ripping_file_p,
            'total_percent':self._ripping_total_p
        }
        return return_dict
##########
##CHECKS##
##########

#######################
##DATABASE & API CALL##
#######################

#####################
##MUSICBRAINZ CALLS##
#####################
    def _get_musicbrainz_disc_id(self):
        '''gets the musicbrainz disc id'''
        self._disc_id = discid.read(self._device).id

#####################
##DISC RIP COMMANDS##
#####################
    @abstractmethod
    def rip_disc(self, track_count):
        '''command to rip the cd here'''

##########
##Script##
##########
    def run(self):
        '''script to rip audio cd'''
