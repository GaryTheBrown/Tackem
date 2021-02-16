'''Special Linux Drive Functions'''
from libs.ripper.ISO.iso import ISORipper

# from .audiocd_linux import AudioCDLinux
# from .video_linux import VideoLinux


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
        # self._ripper = VideoLinux(self.get_device(), self._thread.getName(),
        #                           self._disc_type, self._set_drive_status, self._thread_run)
