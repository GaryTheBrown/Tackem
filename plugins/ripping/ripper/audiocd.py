'''Audio Ripping Feature'''
from abc import ABCMeta, abstractmethod
import discid
from .data.events import RipperEvents

class Audio(metaclass=ABCMeta):
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

###########
##SETTERS##
###########

###########
##GETTERS##
###########

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
    def rip_disc(self):
        '''command to rip the cd here'''

##########
##Script##
##########
    def run(self):
        '''script to rip audio cd'''
