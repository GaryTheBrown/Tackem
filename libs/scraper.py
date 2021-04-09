"""Scraper System"""
import requests

from data.config import CONFIG
from libs.classproperty import classproperty


class Scraper:
    """Scraper html System Here"""

    __base_url = ""
    __image_config: dict = {}
    __working = False

    __headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=utf-8",
        "User-Agent": "tackem/0.0.1",
    }

    @classmethod
    def start(cls):
        if cls.__base_url != "":
            return
        cls.__base_url = CONFIG["scraper"]["url"].value
        if CONFIG["scraper"]["v4apikey"].value:
            cls.__headers["Authorization"] = "Bearer " + CONFIG["scraper"]["v4apikey"].value
        cls.__image_config = cls.__get("/3/configuration")["images"]
        cls.__working = bool(cls.__image_config)

    @classproperty
    def working(cls) -> bool:
        """returns if the system is working"""
        return cls.__working

    @classproperty
    def image_base(cls) -> str:
        """returns the base address for the image"""
        return cls.__image_config["secure_base_url"]

    @classproperty
    def image_config(cls) -> dict:
        """returns the image config for urls"""
        return cls.__image_config

    @classmethod
    def __get(cls, url: str, **params: dict) -> dict:
        """get with url creation"""
        if CONFIG["scraper"]["language"].value:
            params["language"] = CONFIG["scraper"]["language"].value

        r = requests.get(cls.__base_url + url, params=params, headers=cls.__headers)
        r.raise_for_status()
        return r.json()

    @classmethod
    def __post(cls, url: str, **data: dict) -> dict:
        """get with url creation"""
        if CONFIG["scraper"]["language"].value:
            data["language"] = CONFIG["scraper"]["language"].value

        r = requests.post(cls.__base_url + url, data=data, headers=cls.__headers)
        r.raise_for_status()
        return r.json()

    @classmethod
    def search_for_movie(cls, query: str, page: int = 1, year: int = None) -> dict:
        """searches for a movie getting all options"""
        query_to_go = query.replace(" ", "+")
        return cls.__get("/3/search/movie", page=page, query=query_to_go, year=year)

    @classmethod
    def search_by_imdb_id(cls, imdb_id) -> dict:
        """searches by the IMDB ID"""
        return cls.__get(f"/3/find/{imdb_id}", external_source="imdb_id")

    @classmethod
    def get_movie_details(cls, movie_id) -> dict:
        """returns the full movie details"""
        return cls.__get(f"/3/movie/{movie_id}")

    @classmethod
    def search_for_tvshow(cls, query: str, page: int = 1) -> dict:
        """searches for a movie getting all options"""
        query_to_go = query.replace(" ", "+")
        return cls.__get("/3/search/tv", page=page, query=query_to_go)

    @classmethod
    def search_by_tvdb_id(cls, tvdb_id) -> dict:
        """searches by the TVDB ID"""
        return cls.__get(f"/3/find/{tvdb_id}", external_source="tvdb_id")

    @classmethod
    def get_tvshow_details(cls, tvshow_id) -> dict:
        """returns the full tv show details"""
        return cls.__get(f"/3/tv/{tvshow_id}", append_to_response="external_ids")

    @classmethod
    def get_tvshow_episode_details(cls, tvshow_id, season, episode) -> dict:
        """returns the full tv show details"""
        return cls.__get(f"/3/tv/{tvshow_id}/season/{season}/episode/{episode}")
