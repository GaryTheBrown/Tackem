"""Scraper System"""
import requests
from playhouse.shortcuts import model_to_dict

from config import CONFIG
from database.library.base import LibraryBaseCompanies
from database.library.base_movie import LibraryBaseCollection
from database.library.base_movie import LibraryBaseMovie
from database.library.base_movie import LibraryBaseMovieGenres
from database.library.base_movie import LibraryBaseMovieProductionCompanies
from database.library.base_movie import LibraryBaseMovieProductionCountries
from database.library.base_movie import LibraryBaseMovieSpokenLanguages
from database.scraper import ScraperCountries
from database.scraper import ScraperGenreMovies
from database.scraper import ScraperGenreTVShow
from libs import classproperty


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

        if ScraperCountries.table_setup():
            countries = cls.__get("/3/configuration/countries")
            ScraperCountries.insert_many(countries).execute()
        if ScraperGenreMovies.table_setup():
            genre_movies = cls.__get("/3/genre/movie/list")["genres"]
            ScraperGenreMovies.insert_many(genre_movies).execute()
        if ScraperGenreTVShow.table_setup():
            genre_tvshows = cls.__get("/3/genre/tv/list")["genres"]
            ScraperGenreTVShow.insert_many(genre_tvshows).execute()

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
    def search_for_tvshow(cls, query: str, page: int = 1) -> dict:
        """searches for a movie getting all options"""
        query_to_go = query.replace(" ", "+")
        return cls.__get("/3/search/tv", page=page, query=query_to_go)

    @classmethod
    def tvdb_id(cls, tvdb_id) -> dict:
        """searches by the TVDB ID"""
        return cls.__get(f"/3/find/{tvdb_id}", external_source="tvdb_id")

    @classmethod
    def imdb_id(cls, imdb_id) -> dict:
        """searches by the TVDB ID"""
        return cls.__get(f"/3/find/{imdb_id}", external_source="imdb_id")

    @classmethod
    def get_movie_details(cls, tmdb_id: int) -> dict:
        """returns the full movie details"""
        movie = LibraryBaseMovie.get_or_none(LibraryBaseMovie.id == tmdb_id)
        if movie:
            return model_to_dict(movie, backrefs=True)

        data = cls.__get(f"/3/movie/{tmdb_id}")
        movie = LibraryBaseMovie()
        movie.id = tmdb_id

        movie.backdrop_path = data.get("backdrop_path", None)
        movie.budget = data["budget"]
        movie.homepage = data.get("homepage", None)
        movie.imdb_id = data.get("imdb_id", None)
        movie.original_language = data["original_language"]
        movie.original_title = data["original_title"]
        movie.overview = data.get("overview", None)
        movie.popularity = data["popularity"]
        movie.poster_path = data.get("poster_path", None)
        movie.release_date = data["release_date"]
        movie.revenue = data["revenue"]
        movie.runtime = data.get("runtime", None)
        movie.status = data["status"]
        movie.tagline = data.get("tagline", None)
        movie.title = data["title"]
        movie.video = data["video"]
        movie.vote_average = data["vote_average"]
        movie.vote_count = data["vote_count"]

        if (coldata := data.get("belongs_to_collection", None)) is not None:
            collection = LibraryBaseCollection()
            collection.id = coldata["id"]
            collection.name = coldata["name"]
            collection.poster_path = coldata["poster_path"]
            collection.backdrop_path = coldata["backdrop_path"]
            collection.save()
            movie.belongs_to_collection = collection

        movie.save()

        for genre in data["genres"]:
            genre = ScraperGenreMovies.get_by_id(genre["id"])
            LibraryBaseMovieGenres.create(movie=movie, genre=genre)

        for compdata in data["production_companies"]:
            company = LibraryBaseCompanies()
            company.id = compdata["id"]
            company.logo_path = compdata["logo_path"]
            company.name = compdata["name"]
            company.origin_country = compdata["origin_country"]
            company.save()
            LibraryBaseMovieProductionCompanies.create(movie=movie, company=company)

        for countrypdata in data["production_countries"]:
            country = ScraperCountries.get(iso_3166_1=countrypdata["iso_3166_1"])
            LibraryBaseMovieProductionCountries.create(movie=movie, country=country)

        for spokendata in data["spoken_languages"]:
            lang = LibraryBaseMovieSpokenLanguages()
            lang.movie = movie
            lang.iso_639_1 = spokendata["iso_639_1"]
            lang.save()

        return data

    @classmethod
    def get_tvshow_details(cls, tvshow_id: int) -> dict:
        """returns the full tv show details"""
        return cls.__get(f"/3/tv/{tvshow_id}", append_to_response="external_ids")

    @classmethod
    def get_tvshow_season_details(cls, tvshow_id: int, season: int) -> dict:
        """returns the full tv show details"""
        return cls.__get(f"/3/tv/{tvshow_id}/season/{season}")

    @classmethod
    def get_tvshow_episode_details(cls, tvshow_id: int, season: int, episode: int) -> dict:
        """returns the full tv show details"""
        return cls.__get(f"/3/tv/{tvshow_id}/season/{season}/episode/{episode}")
