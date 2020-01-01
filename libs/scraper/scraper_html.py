'''Scraper System'''
import os
import cherrypy
from libs.scraper.scraper_base import Scraper


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
        return java_file.replace("%%BASEURL%%", self._tackem_system.baseurl)
