'''Scraper System'''
import http.client
import json

class Scraper():
    '''Scraper html System Here'''
    def __init__(self, config):
        self._config = config
        self._apikey = config['scraper']['apikey']
        self._language = config['scraper']['language']
        self._include_adult = config['scraper']['includeadult']
        self._conn = http.client.HTTPSConnection(config['scraper']['url'])
        self._image_config = self._configuration()

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

#################
##MOVIE SECTION##
#################
    def search_for_movie(self, query, page=1, year=None):
        '''searches for a movie getting all options'''
        query_to_go = query.replace(" ", "+")
        command = "/3/search/movie?" + self._base() + "&page=" + str(page)
        command += "&query=" + query_to_go
        if year:
            command += "&year=" + str(year)
        return self._get_request(command)

    def search_by_imdb_id(self, imdb_id):
        '''searches by the IMDB ID'''
        command = "/3/find/" + str(imdb_id) + "?" + self._base(adult=False)
        command += "&external_source=imdb_id"
        return self._get_request(command)

    def get_movie_details(self, movie_id):
        '''returns the full movie details'''
        command = "/3/movie/" + str(movie_id) + "?" + self._base(adult=False)
        return self._get_request(command)

##################
##TVSHOW SECTION##
##################
    def search_for_tvshow(self, query, page=1):
        '''searches for a movie getting all options'''
        query_to_go = query.replace(" ", "+")
        command = "/3/search/tv?" + self._base(adult=False) + "&page=" + str(page)
        command += "&query=" + query_to_go
        return self._get_request(command)

    def search_by_tvdb_id(self, imdb_id):
        '''searches by the TVDB ID'''
        command = "/3/find/" + str(imdb_id) + "?" + self._base(adult=False)
        command += "&external_source=tvdb_id"
        return self._get_request(command)

    def get_tvshow_details(self, tvshow_id):
        '''returns the full tv show details'''
        command = "/3/tv/" + str(tvshow_id) + "?" + self._base(adult=False)
        command += "&append_to_response=external_ids"
        return self._get_request(command)

############
##REQUESTS##
############
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
