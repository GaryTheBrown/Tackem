'''Scraper System'''
import http.client
import json
from config_data import CONFIG


class Scraper():
    '''Scraper html System Here'''


    def __init__(self):
        self.__apikey = CONFIG['scraper']['apikey'].value
        self.__language = CONFIG['scraper']['language'].value
        self.__include_adult = CONFIG['scraper']['includeadult'].value
        self.__conn = http.client.HTTPSConnection(CONFIG['scraper']['url'].value)
        self._image_config = self._configuration()


###########
##GETTERS##
###########


    def image_base(self) -> str:
        '''returns the base address for the image'''
        return self._image_config['secure_base_url']


#############
##SHORTCUTS##
#############


    def __base(self, adult: bool = True, language: bool = True) -> str:
        '''creates the base command keys'''
        base = "api_key=" + self.__apikey
        if adult:
            base += "&include_adult=" + str(self.__include_adult).lower()
        if language:
            base += "&language=" + self.__language
        return base


    def __fail_print(self, status: str, reason: str) -> str:
        '''message returned when the scraper failed'''
        return "Search Failed\nStatus: " + status + "\nReason: " + reason + "\n"


############
##COMMANDS##
############


    def _configuration(self):
        '''config section for startup getting info mainly image urls'''
        command = "/3/configuration?" + self.__base(False, False)
        data = self.__get_request(command)
        if data['success'] is False:
            print("ERROR IN SCRAPER STARTUP:", self.__fail_print(data['status'], data['reason']))
            return None
        return data['response']['images']


#################
##MOVIE SECTION##
#################


    def search_for_movie(self, query: str, page: int = 1, year: int = None) -> dict:
        '''searches for a movie getting all options'''
        query_to_go = query.replace(" ", "+")
        command = "/3/search/movie?" + self.__base() + "&page=" + str(page)
        command += "&query=" + query_to_go
        if year:
            command += "&year=" + str(year)
        return self.__get_request(command)


    def search_by_imdb_id(self, imdb_id) -> dict:
        '''searches by the IMDB ID'''
        command = "/3/find/" + str(imdb_id) + "?" + self.__base(adult=False)
        command += "&external_source=imdb_id"
        return self.__get_request(command)


    def get_movie_details(self, movie_id) -> dict:
        '''returns the full movie details'''
        command = "/3/movie/" + str(movie_id) + "?" + self.__base(adult=False)
        return self.__get_request(command)


##################
##TVSHOW SECTION##
##################


    def search_for_tvshow(self, query: str, page: int = 1) -> dict:
        '''searches for a movie getting all options'''
        query_to_go = query.replace(" ", "+")
        command = "/3/search/tv?" + self.__base(adult=False) + "&page=" + str(page)
        command += "&query=" + query_to_go
        return self.__get_request(command)


    def search_by_tvdb_id(self, imdb_id) -> dict:
        '''searches by the TVDB ID'''
        command = "/3/find/" + str(imdb_id) + "?" + self.__base(adult=False)
        command += "&external_source=tvdb_id"
        return self.__get_request(command)


    def get_tvshow_details(self, tvshow_id) -> dict:
        '''returns the full tv show details'''
        command = "/3/tv/" + str(tvshow_id) + "?" + self.__base(adult=False)
        command += "&append_to_response=external_ids"
        return self.__get_request(command)


    def get_tvshow_episode_details(self, tvshow_id, season, episode) -> dict:
        '''returns the full tv show details'''
        command = "/3/tv/" + str(tvshow_id) + "/season/" + str(season) + "/episode/" + str(episode)
        command += "?" + self.__base(adult=False)
        return self.__get_request(command)


############
##REQUESTS##
############


    def __get_request(self, command: str) -> dict:
        '''do a get request'''
        self.__conn.request("GET", command)
        response = self.__conn.getresponse()
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
