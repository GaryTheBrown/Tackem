"""Scraper System"""
from http.client import HTTPSConnection
import json
from libs.classproperty import classproperty
from data.config import CONFIG


class Scraper:
    """Scraper html System Here"""

    __conn: HTTPSConnection = None
    __image_config: dict = {}
    __working = False

    @classmethod
    def start(cls):
        cls.__conn = HTTPSConnection(CONFIG["scraper"]["url"].value)
        cls.__image_config = cls.__configuration()
        cls.__working = bool(cls.__image_config)

    @classproperty
    def working(cls) -> bool:
        """returns if the system is working"""
        return cls.__working

    @classproperty
    def image_base(cls) -> str:
        """returns the base address for the image"""
        return cls.__image_config["secure_base_url"]

    @classmethod
    def __base(cls, adult: bool = True, language: bool = True) -> str:
        """creates the base command keys"""
        base = "api_key=" + CONFIG["scraper"]["apikey"].value
        if adult:
            base += (
                f"&include_adult={str(CONFIG['scraper']['includeadult'].value).lower()}"
            )
        if language:
            base += f"&language={CONFIG['scraper']['language'].value}"
        return base

    @classmethod
    def __fail_print(cls, status: str, reason: str) -> str:
        """message returned when the scraper failed"""
        return f"Search Failed\nStatus: {status}\nReason: {reason}\n"

    @classmethod
    def __configuration(cls):
        """config section for startup getting info mainly image urls"""
        command = f"/3/configuration?{cls.__base(False, False)}"
        data = cls.__get_request(command)
        if data["success"] is False:
            if data["status"] != 401:
                print(
                    "ERROR IN SCRAPER STARTUP:",
                    cls.__fail_print(data["status"], data["reason"]),
                )
            return None
        return data["response"]["images"]

    @classmethod
    def __get_request(cls, command: str) -> dict:
        """do a get request"""
        cls.__conn.request("GET", command)
        response = cls.__conn.getresponse()
        return_data = {"status": int(response.status), "reason": response.reason}
        success = int(response.status) == 200 and response.reason == "OK"
        return_data["success"] = success
        if success:
            return_data["response"] = json.loads(response.read().decode("utf-8"))
        return return_data

    @classmethod
    def search_for_movie(cls, query: str, page: int = 1, year: int = None) -> dict:
        """searches for a movie getting all options"""
        query_to_go = query.replace(" ", "+")
        command = f"/3/search/movie?{cls.__base()}&page={str(page)}&query={query_to_go}"
        if year:
            command += f"&year={str(year)}"
        return cls.__get_request(command)

    @classmethod
    def search_by_imdb_id(cls, imdb_id) -> dict:
        """searches by the IMDB ID"""
        return cls.__get_request(
            f"/3/find/{str(imdb_id)}?{cls.__base(adult=False)}&external_source=imdb_id"
        )

    @classmethod
    def get_movie_details(cls, movie_id) -> dict:
        """returns the full movie details"""
        return cls.__get_request(f"/3/movie/{str(movie_id)}?{cls.__base(adult=False)}")

    @classmethod
    def search_for_tvshow(cls, query: str, page: int = 1) -> dict:
        """searches for a movie getting all options"""
        query_to_go = query.replace(" ", "+")
        return cls.__get_request(
            f"/3/search/tv?{cls.__base(adult=False)}&page={str(page)}&query={query_to_go}"
        )

    @classmethod
    def search_by_tvdb_id(cls, imdb_id) -> dict:
        """searches by the TVDB ID"""
        return cls.__get_request(
            f"/3/find/{str(imdb_id)}?{cls.__base(adult=False)}&external_source=tvdb_id"
        )

    @classmethod
    def get_tvshow_details(cls, tvshow_id) -> dict:
        """returns the full tv show details"""
        return cls.__get_request(
            f"/3/tv/{str(tvshow_id)}?{cls.__base(adult=False)}&append_to_response=external_ids"
        )

    @classmethod
    def get_tvshow_episode_details(cls, tvshow_id, season, episode) -> dict:
        """returns the full tv show details"""
        return cls.__get_request(
            f"/3/tv/{str(tvshow_id)}/season/{str(season)}"
            + f"/episode/{str(episode)}?{cls.__base(adult=False)}"
        )
