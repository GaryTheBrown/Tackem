'''Special Linux Drive Functions'''
from libs.ripper.makemkv.linux import MakeMKVLinux

class ISORipperLinux(ISORipper):
    '''Drive Control ripper program self contained'''

##########
##Script##
##########
    def _audio_rip(self):
        '''script to rip an audio cd'''
        # self._ripper = AudioCDLinux(self.get_device(), self._thread.getName(),
                                    # self._set_drive_status, self._thread_run)

    def _video_rip(self):
        '''script to rip video disc'''
        self._ripper = MakeMKVLinux(self.__db_id)
