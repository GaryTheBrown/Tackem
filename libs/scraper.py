'''Scraper System'''
import http.client
import json
from config_data import CONFIG

class Scraper:
    '''Scraper html System Here'''

    def __init__(self):
        self.__apikey = CONFIG['scraper']['apikey'].value
        self.__language = CONFIG['scraper']['language'].value
        self.__include_adult = CONFIG['scraper']['includeadult'].value
        self.__conn = http.client.HTTPSConnection(
            CONFIG['scraper']['url'].value)
        self._image_config = self._configuration()
        self.__working = bool(self._image_config)

###########
##GETTERS##
###########
    @property
    def working(self) -> bool:
        '''returns if the system is working'''
        return self.__working

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
            base += f"&include_adult={str(self.__include_adult).lower()}"
        if language:
            base += f"&language={self.__language}"
        return base

    def __fail_print(self, status: str, reason: str) -> str:
        '''message returned when the scraper failed'''
        return f"Search Failed\nStatus: {status}\nReason: {reason}\n"

############
##COMMANDS##
############
    def _configuration(self):
        '''config section for startup getting info mainly image urls'''
        command = f"/3/configuration?{self.__base(False, False)}"
        data = self.__get_request(command)
        if data['success'] is False:
            if data["status"] != 401:
                print(
                    "ERROR IN SCRAPER STARTUP:",
                    self.__fail_print(
                        data['status'], data['reason']
                    )
                )
            return None
        return data['response']['images']

#################
##MOVIE SECTION##
#################
    def search_for_movie(self, query: str, page: int = 1, year: int = None) -> dict:
        '''searches for a movie getting all options'''
        query_to_go = query.replace(" ", "+")
        command = f"/3/search/movie?{self.__base()}&page={str(page)}&query={query_to_go}"
        if year:
            command += f"&year={str(year)}"
        return self.__get_request(command)

    def search_by_imdb_id(self, imdb_id) -> dict:
        '''searches by the IMDB ID'''
        return self.__get_request(
            f"/3/find/{str(imdb_id)}?{self.__base(adult=False)}&external_source=imdb_id"
        )

    def get_movie_details(self, movie_id) -> dict:
        '''returns the full movie details'''
        return self.__get_request(
            f"/3/movie/{str(movie_id)}?{self.__base(adult=False)}"
        )

##################
##TVSHOW SECTION##
##################
    def search_for_tvshow(self, query: str, page: int = 1) -> dict:
        '''searches for a movie getting all options'''
        query_to_go = query.replace(" ", "+")
        return self.__get_request(
            f"/3/search/tv?{self.__base(adult=False)}&page={str(page)}&query={query_to_go}"
        )

    def search_by_tvdb_id(self, imdb_id) -> dict:
        '''searches by the TVDB ID'''
        return self.__get_request(
            f"/3/find/{str(imdb_id)}?{self.__base(adult=False)}&external_source=tvdb_id"
        )

    def get_tvshow_details(self, tvshow_id) -> dict:
        '''returns the full tv show details'''
        return self.__get_request(
            f"/3/tv/{str(tvshow_id)}?{self.__base(adult=False)}&append_to_response=external_ids"
        )

    def get_tvshow_episode_details(self, tvshow_id, season, episode) -> dict:
        '''returns the full tv show details'''
        return self.__get_request(
            f"/3/tv/{str(tvshow_id)}/season/{str(season)}" \
                + f"/episode/{str(episode)}?{self.__base(adult=False)}"
        )

############
##REQUESTS##
############
    def __get_request(self, command: str) -> dict:
        '''do a get request'''
        self.__conn.request("GET", command)
        response = self.__conn.getresponse()
        return_data = {
            "status": int(response.status),
            "reason": response.reason
        }
        success = int(response.status) == 200 and response.reason == "OK"
        return_data['success'] = success
        if success:
            return_data['response'] = json.loads(
                response.read().decode("utf-8"))
        return return_data

SCRAPER = Scraper()
