'''Scraper System'''
import http.client
import json
import os
import cherrypy
from libs import html_parts as ghtml_parts
from libs.data.languages import Languages
from system.root import TackemSystemRoot
from . import html_parts
from .scraper_html import ScraperHtml
from .ripper import ScraperRipper


def mounts():
    '''where the system creates the cherrypy mounts'''
    scraper = ScraperHtml()
    scraper.ripper = ScraperRipper()
    cherrypy.tree.mount(scraper, TackemSystemRoot('scraper').baseurl + "scraper/")
