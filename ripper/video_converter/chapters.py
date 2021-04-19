"""Video Controller Chapters code"""
from ripper.video_converter.base import VideoConverterBase


class VideoConverterChapters(VideoConverterBase):
    """Video Controller Chapters code"""

    def _sort_chapters(self, has_chapters: bool):
        """sorts out the chapters"""
        if has_chapters:
            self._command.append("-map_chapters")
            if self._conf["chapters"]["keepchapters"].value:
                self._command.append("0")
            else:
                self._command.append("-1")
