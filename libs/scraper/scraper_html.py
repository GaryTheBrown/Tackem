'''Scraper System'''
import os
import cherrypy
from libs.scraper.scraper_base import Scraper
from config_data import CONFIG

class ScraperHtml(Scraper):
    '''Scraper html System Here'''


    @cherrypy.expose
    def index(self) -> str:
        '''index of scraper'''
        return "RUNNING"


    @cherrypy.expose
    def javascript(self) -> str:
        '''index of scraper'''
        java_file = str(open(os.path.dirname(__file__) + "/javascript/base.js", "r").read())
        return java_file.replace("%%BASEURL%%", CONFIG['webui']['baseurl'].value)
