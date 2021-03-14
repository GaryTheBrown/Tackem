'''Upload Partials'''
from libs.html_system import HTMLSystem


class PartialsUpload:
    '''Upload Partials'''

    @classmethod
    def audio_iso(cls):
        '''returns a partial for audio upload'''
        return HTMLSystem.part(
            "partial/uploads/audioiso"
        )

    @classmethod
    def video_iso(cls):
        '''returns a partial for video upload'''
        return HTMLSystem.part(
            "partial/uploads/videoiso"
        )
