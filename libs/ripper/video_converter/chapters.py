'''Video Controller Chapters code'''
from libs.ripper.ffprobe import FFprobe
from libs.ripper.video_converter.base import VideoConverterBase

class VideoConverterChapters(VideoConverterBase):
    '''Video Controller Chapters code'''

    def _sort_chapters(self, probe_info: FFprobe):
        '''sorts out the chapters'''
        if probe_info.has_chapters():
            self._command.append("-map_chapters")
            if self._conf['chapters']['keepchapters'].value:
                self._command.append("0")
            else:
                self._command.append("-1")
