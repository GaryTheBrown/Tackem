"""Scraper System"""
import requests

from config import CONFIG
from database.scraper import ScraperCompanies
from database.scraper import ScraperCountries
from database.scraper import ScraperGenreMovies
from database.scraper import ScraperGenreTVShows
from database.scraper import ScraperNetworks
from database.scraper.collection import ScraperCollection
from database.scraper.collection.part import ScraperCollectionPart
from database.scraper.collection.part_genres import ScraperCollectionPartGenres
from database.scraper.movie import ScraperMovie
from database.scraper.movie.cast import ScraperMovieCast
from database.scraper.movie.genres import ScraperMovieGenres
from database.scraper.movie.production_companies import ScraperMovieProductionCompanies
from database.scraper.movie.production_countries import ScraperMovieProductionCountries
from database.scraper.movie.spoken_languages import ScraperMovieSpokenLanguages
from database.scraper.tvshow import ScraperTVShow
from database.scraper.tvshow.cast import ScraperTVShowCast
from database.scraper.tvshow.created_by import ScraperTVShowCreatedBy
from database.scraper.tvshow.episode import ScraperTVShowEpisode
from database.scraper.tvshow.episode_run_time import ScraperTVShowEpisodeRunTime
from database.scraper.tvshow.genres import ScraperTVShowGenres
from database.scraper.tvshow.guest_stars import ScraperTVShowGuestStars
from database.scraper.tvshow.languages import ScraperTVShowLanguages
from database.scraper.tvshow.networks import ScraperTVShowNetworks
from database.scraper.tvshow.origin_country import ScraperTVShowOriginCountry
from database.scraper.tvshow.production_companies import ScraperTVShowProductionCompanies
from database.scraper.tvshow.production_countries import ScraperTVShowProductionCountries
from database.scraper.tvshow.season import ScraperTVShowSeason
from database.scraper.tvshow.spoken_languages import ScraperTVShowSpokenLanguages
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
        if ScraperGenreTVShows.table_setup():
            genre_tvshows = cls.__get("/3/genre/tv/list")["genres"]
            ScraperGenreTVShows.insert_many(genre_tvshows).execute()

        ScraperCompanies.table_setup()
        ScraperNetworks.table_setup()

        ScraperCollection.table_setup()
        ScraperCollectionPart.table_setup()
        ScraperCollectionPartGenres.table_setup()

        ScraperMovie.table_setup()
        ScraperMovieGenres.table_setup()
        ScraperMovieProductionCompanies.table_setup()
        ScraperMovieProductionCountries.table_setup()
        ScraperMovieSpokenLanguages.table_setup()
        ScraperMovieCast.table_setup()

        ScraperTVShow.table_setup()
        ScraperTVShowCreatedBy.table_setup()
        ScraperTVShowEpisodeRunTime.table_setup()
        ScraperTVShowGenres.table_setup()
        ScraperTVShowLanguages.table_setup()
        ScraperTVShowNetworks.table_setup()
        ScraperTVShowOriginCountry.table_setup()
        ScraperTVShowProductionCompanies.table_setup()
        ScraperTVShowProductionCountries.table_setup()
        ScraperTVShowSeason.table_setup()
        ScraperTVShowSpokenLanguages.table_setup()
        ScraperTVShowEpisode.table_setup()
        ScraperTVShowCast.table_setup()
        ScraperTVShowGuestStars.table_setup()

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
    def get_movie_details(cls, tmdb_id: int) -> ScraperMovie:
        """returns the full movie details"""
        movie = ScraperMovie.get_or_none(ScraperMovie.id == tmdb_id)
        if movie:
            return movie

        data = cls.__get(f"/3/movie/{tmdb_id}", append_to_response="credits")
        movie = ScraperMovie()
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
            collection = ScraperCollection()
            collection.id = coldata["id"]
            collection.name = coldata["name"]
            collection.poster_path = coldata["poster_path"]
            collection.backdrop_path = coldata["backdrop_path"]
            collection.save()
            movie.belongs_to_collection = collection

        movie.save()

        for genre in data["genres"]:
            genre = ScraperGenreMovies.get_by_id(genre["id"])
            ScraperMovieGenres.create(movie=movie, genre=genre)

        for compdata in data["production_companies"]:
            company = ScraperCompanies()
            company.id = compdata["id"]
            company.logo_path = compdata["logo_path"]
            company.name = compdata["name"]
            company.origin_country = compdata["origin_country"]
            company.save()
            ScraperMovieProductionCompanies.create(movie=movie, company=company)

        for countrypdata in data["production_countries"]:
            country = ScraperCountries.get(iso_3166_1=countrypdata["iso_3166_1"])
            ScraperMovieProductionCountries.create(movie=movie, country=country)

        for spokendata in data["spoken_languages"]:
            lang = ScraperMovieSpokenLanguages()
            lang.movie = movie
            lang.iso_639_1 = spokendata["iso_639_1"]
            lang.save()

        if "credits" in data and "cast" in data["credits"]:
            for castData in data["credits"]["cast"]:
                cast = ScraperMovieCast.get_or_create(id=castData["id"])
                cast.gender = castData["gender"]
                cast.known_for_department = castData["known_for_department"]
                cast.name = castData["name"]
                cast.original_name = castData["original_name"]
                cast.popularity = castData["popularity"]
                cast.profile_path = castData["profile_path"]
                cast.cast_id = castData["cast_id"]
                cast.character = castData["character"]
                cast.credit_id = castData["credit_id"]
                cast.order = castData["order"]
                cast.save()

        return ScraperMovie.get_or_none(ScraperMovie.id == tmdb_id)

    @classmethod
    def get_tvshow_details(cls, tmdb_id: int) -> ScraperTVShow:
        """returns the full tv show details"""
        tvshow = ScraperTVShow.get_or_none(ScraperTVShow.id == tmdb_id)
        if tvshow:
            return tvshow
        data = cls.__get(f"/3/tv/{tmdb_id}", append_to_response="credits")

        tvshow = ScraperTVShow()
        tvshow.id = data["id"]

        return ScraperTVShow.get_or_none(ScraperTVShow.id == tmdb_id)

    @classmethod
    def get_tvshow_season_details(cls, tvshow_id: int, season: int) -> dict:
        """returns the full tv show details"""
        return cls.__get(f"/3/tv/{tvshow_id}/season/{season}")

    @classmethod
    def get_tvshow_episode_details(cls, tvshow_id: int, season: int, episode: int) -> dict:
        """returns the full tv show details"""
        return cls.__get(f"/3/tv/{tvshow_id}/season/{season}/episode/{episode}")
