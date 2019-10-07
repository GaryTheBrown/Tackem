'''Audio Ripping Feature'''
import musicbrainzngs
from system.root import TackemSystemRoot
from libs.startup_arguments import PROGRAMNAME, PROGRAMVERSION, PROGRAMGITADDRESS


class MusicBrainz():
    '''video ripping controller'''


    def __init__(self):
        self.__tackem_system = TackemSystemRoot('musicbrainz')
        if self.__tackem_system.config().get('enabled', False):
            self.__logged_in = False
            musicbrainzngs.set_useragent(PROGRAMNAME, PROGRAMVERSION, PROGRAMGITADDRESS)
            musicbrainzngs.set_hostname(self.__tackem_system.config()['url'])
            musicbrainzngs.set_caa_hostname(self.__tackem_system.config()['coverarturl'])
            if self.__tackem_system.config()['username'] != "":
                if self.__tackem_system.config()['password'] != "":
                    musicbrainzngs.auth(self.__tackem_system.config()['username'],
                                        self.__tackem_system.config()['password'])
            self.__logged_in = True


    #https://python-musicbrainzngs.readthedocs.io/en/v0.6/
    def get_data_for_discid(self, disc_id):
        '''get data by disc id'''
        includes = ["artists", "recordings", "artist-credits"]
        return musicbrainzngs.get_releases_by_discid(disc_id, includes=includes).get('disc', {})
