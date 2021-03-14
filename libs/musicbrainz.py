'''Audio Ripping Feature'''
import musicbrainzngs
from data import PROGRAMNAME, PROGRAMVERSION, PROGRAMGITADDRESS
from data.config import CONFIG


class MusicBrainz():
    '''video ripping controller'''

    def __init__(self):
        # self.__tackem_system = TackemSystemRoot('musicbrainz')
        self.__logged_in = False
        if CONFIG['musicbrainz']['username'].value == "":
            return
        if CONFIG['musicbrainz']['password'].value == "":
            return
        musicbrainzngs.set_useragent(
            PROGRAMNAME, PROGRAMVERSION, PROGRAMGITADDRESS)
        musicbrainzngs.set_hostname(CONFIG['musicbrainz']['url'].value)
        musicbrainzngs.set_caa_hostname(
            CONFIG['musicbrainz']['coverarturl'].value)
        if CONFIG['musicbrainz']['username'].value != "":
            if CONFIG['musicbrainz']['password'].value != "":
                musicbrainzngs.auth(CONFIG['musicbrainz']['username'].value,
                                    CONFIG['musicbrainz']['password'].value)
        self.__logged_in = True

    # https://python-musicbrainzngs.readthedocs.io/en/v0.6/

    def get_data_for_discid(self, disc_id: int):
        '''get data by disc id'''
        if not self.__logged_in:
            return {}
        includes = ["artists", "recordings", "artist-credits"]
        return musicbrainzngs.get_releases_by_discid(disc_id, includes=includes).get('disc', {})


MUSICBRAINZ = MusicBrainz()
