'''Scraper System'''
import http.client
import json
import os
import cherrypy
from config_data import CONFIG
from libs.scraper.scraper_html import ScraperHtml
from libs.scraper.ripper import ScraperRipper


def mounts() -> None:
    '''where the system creates the cherrypy mounts'''
    scraper = ScraperHtml()
    scraper.ripper = ScraperRipper()
    cherrypy.tree.mount(scraper, CONFIG['webui']['baseurl'].value + "scraper/")
