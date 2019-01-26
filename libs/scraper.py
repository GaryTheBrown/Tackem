'''Scraper System'''
import cherrypy

class Scraper():
    '''Scraper System Here'''

    def __init__(self, config):
        self._apikey = config['scraper']['apikey']
        self._language = config['scraper']['language']
        self._include_adult = config['scraper']['includeadult']

    @cherrypy.expose
    def index(self):
        '''index of scraper'''
        return "RUNNING"
