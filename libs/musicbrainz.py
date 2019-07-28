'''Audio Ripping Feature'''
import musicbrainzngs
from libs.startup_arguments import PROGRAMNAME, PROGRAMVERSION, PROGRAMGITADDRESS

class MusicBrainz():
    '''video ripping controller'''
    def __init__(self, config):
        self._config = config
        self._logged_in = False
        musicbrainzngs.set_useragent(PROGRAMNAME, PROGRAMVERSION, PROGRAMGITADDRESS)
        musicbrainzngs.set_hostname(self._config['url'])
        musicbrainzngs.set_caa_hostname(self._config['coverarturl'])
        if self._config['username'] != "" and self._config['password'] != "":
            musicbrainzngs.auth(self._config['username'], self._config['password'])
            self._logged_in = True

    #https://python-musicbrainzngs.readthedocs.io/en/v0.6/
    def get_data_for_discid(self, disc_id):
        '''get data by disc id'''
        includes = ["artists", "recordings", "artist-credits"]
        return musicbrainzngs.get_releases_by_discid(disc_id, includes=includes).get('disc', {})
