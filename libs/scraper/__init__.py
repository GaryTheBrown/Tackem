'''Scraper System'''
import http.client
import json
import os
import cherrypy
from libs import html_parts as ghtml_parts
from libs.data.languages import Languages
from . import html_parts
from .scraper_html import ScraperHtml
from .ripper import ScraperRipper

def mounts(config):
    '''where the system creates the cherrypy mounts'''
    scraper = ScraperHtml(config)
    scraper.ripper = ScraperRipper(config)
    cherrypy.tree.mount(scraper, config.get("webui", {}).get("baseurl", "/") + "scraper/")
