'''Audio Ripping Feature'''
import musicbrainzngs
from libs.startup_arguments import PROGRAMNAME, PROGRAMVERSION, PROGRAMGITADDRESS
from config_data import CONFIG


class MusicBrainz():
    '''video ripping controller'''


    def __init__(self):
        # self.__tackem_system = TackemSystemRoot('musicbrainz')
        if CONFIG['musicbrainz']['enabled'].value:
            self.__logged_in = False
            musicbrainzngs.set_useragent(PROGRAMNAME, PROGRAMVERSION, PROGRAMGITADDRESS)
            musicbrainzngs.set_hostname(CONFIG['musicbrainz']['url'].value)
            musicbrainzngs.set_caa_hostname(CONFIG['musicbrainz']['coverarturl'].value)
            if CONFIG['musicbrainz']['username'].value != "":
                if CONFIG['musicbrainz']['password'].value != "":
                    musicbrainzngs.auth(CONFIG['musicbrainz']['username'].value,
                                        CONFIG['musicbrainz']['password'].value)
            self.__logged_in = True


    #https://python-musicbrainzngs.readthedocs.io/en/v0.6/
    def get_data_for_discid(self, disc_id):
        '''get data by disc id'''
        includes = ["artists", "recordings", "artist-credits"]
        return musicbrainzngs.get_releases_by_discid(disc_id, includes=includes).get('disc', {})

MUSICBRAINZ = MusicBrainz()
