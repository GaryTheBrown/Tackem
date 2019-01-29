'''Scraper System'''
import http.client
import json
import os
import cherrypy
from libs import html_parts as ghtml_parts
from libs.data.languages import Languages
from . import html_parts
from .ripper import ScraperRipper

def mounts(config):
    '''where the system creates the cherrypy mounts'''
    scraper = Scraper(config)
    scraper.ripper = ScraperRipper(config)
    cherrypy.tree.mount(scraper, config.get("webui", {}).get("baseurl", "/") + "scraper/")

class Scraper():
    '''Scraper System Here'''

    def __init__(self, config):
        self._config = config
        self._apikey = config['scraper']['apikey']
        self._language = config['scraper']['language']
        self._include_adult = config['scraper']['includeadult']
        self._conn = http.client.HTTPSConnection(config['scraper']['url'])
        self._image_config = self._configuration()

    @cherrypy.expose
    def index(self):
        '''index of scraper'''
        return "RUNNING"

    # @cherrypy.expose
    # def javascript(self):
    #     '''index of scraper'''
    #     java_file = str(open(os.path.dirname(__file__) + "/javascript/base.js", "r").read())
    #     return java_file.replace("%%BASEURL%%", self._config['webui']['baseurl'])

#############
##SHORTCUTS##
#############
    def _base(self, adult=True, language=True):
        '''creates the base command keys'''
        base = "api_key=" + self._apikey
        if adult:
            base += "&include_adult=" + str(self._include_adult).lower()
        if language:
            base += "&language=" + self._language
        return base

    def _fail_print(self, status, reason):
        '''message returned when the scraper failed'''
        return "Search Failed\nStatus: " + status + "\nReason: " + reason + "\n"

############
##COMMANDS##
############
    def _configuration(self):
        '''config section for startup getting info mainly image urls'''
        command = "/3/configuration?" + self._base(False, False)
        data = self._get_request(command)
        if data['success'] is False:
            print("ERROR IN SCRAPER STARTUP:", self._fail_print(data['status'], data['reason']))
            return None
        return data['response']['images']

##############
##HTTP Calls##
##############
    def _get_request(self, command):
        '''do a get request'''
        self._conn.request("GET", command)
        response = self._conn.getresponse()
        return_data = {
            "status":int(response.status),
            "reason":response.reason
        }
        success = int(response.status) == 200 and response.reason == "OK"
        return_data['success'] = success
        if success:
            return_data['response'] = json.loads(response.read().decode("utf-8"))
        return return_data

# payload = "{}"
# conn.request("GET", , payload)
