"""Scraper System"""
import requests

from config import CONFIG
from database.scraper.collection import ScraperCollection
from database.scraper.collection.part import ScraperCollectionPart
from database.scraper.collection.part_genres import ScraperCollectionPartGenres
from database.scraper.company import ScraperCompany
from database.scraper.country import ScraperCountry
from database.scraper.genre.movies import ScraperGenreMovies
from database.scraper.genre.tvshows import ScraperGenreTVShows
from database.scraper.movie import ScraperMovie
from database.scraper.movie.cast import ScraperMovieCast
from database.scraper.movie.genres import ScraperMovieGenres
from database.scraper.movie.production_companies import ScraperMovieProductionCompanies
from database.scraper.movie.production_countries import ScraperMovieProductionCountries
from database.scraper.movie.spoken_languages import ScraperMovieSpokenLanguages
from database.scraper.network import ScraperNetwork
from database.scraper.tvshow import ScraperTVShow
from database.scraper.tvshow.cast import ScraperTVShowCast
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

        if ScraperCountry.table_setup():
            countries = cls.__get("/3/configuration/countries")
            ScraperCountry.insert_many(countries).execute()
        if ScraperGenreMovies.table_setup():
            genre_movies = cls.__get("/3/genre/movie/list")["genres"]
            ScraperGenreMovies.insert_many(genre_movies).execute()
        if ScraperGenreTVShows.table_setup():
            genre_tvshows = cls.__get("/3/genre/tv/list")["genres"]
            ScraperGenreTVShows.insert_many(genre_tvshows).execute()

        ScraperCompany.table_setup()
        ScraperNetwork.table_setup()

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
    def get_movie_details(cls, tmdb_id: int, force_update: bool = False) -> ScraperMovie:
        """returns the full movie details"""

        if not force_update:
            if movie := ScraperMovie.get_or_none(id=tmdb_id):
                return movie

        data = cls.__get(f"/3/movie/{tmdb_id}", append_to_response="credits")

        movie = ScraperMovie.from_data_dict(data)

        if (col_data := data.get("belongs_to_collection", None)) is not None:
            collection = ScraperCollection.from_data_dict(col_data)
            movie.belongs_to_collection = collection
            movie.save()

        for genre_data in data["genres"]:
            genre = ScraperGenreMovies.get_by_id(genre_data["id"])
            ScraperMovieGenres.get_or_create(movie=movie, genre=genre)

        for comp_data in data["production_companies"]:
            company = ScraperCompany.from_data_dict(comp_data)
            ScraperMovieProductionCompanies.get_or_create(movie=movie, company=company)

        for country_data in data["production_countries"]:
            country = ScraperCountry.get(iso_3166_1=country_data["iso_3166_1"])
            ScraperMovieProductionCountries.get_or_create(movie=movie, country=country)

        for spoken_data in data["spoken_languages"]:
            ScraperMovieSpokenLanguages.get_or_create(
                movie=movie, iso_639_1=spoken_data["iso_639_1"]
            )

        if "credits" in data and "cast" in data["credits"]:
            for cast_data in data["credits"]["cast"]:
                ScraperMovieCast.from_data_dict(cast_data, movie)

        return ScraperMovie.get_or_none(id=tmdb_id)

    @classmethod
    def get_tvshow_details(cls, tmdb_id: int, force_update: bool = False) -> ScraperTVShow:
        """returns the full tv show details"""
        if not force_update:
            if tvshow := ScraperTVShow.get_or_none(id=tmdb_id):
                return tvshow

        data = cls.__get(f"/3/tv/{tmdb_id}", append_to_response="credits")
        tvshow = ScraperTVShow.from_data_dict(data)

        # created by

        for time_data in data["epiode_run_time"]:
            ScraperTVShowEpisodeRunTime.get_or_create(tvshow=tvshow, run_time=time_data)

        for genre_data in data["genres"]:
            genre = ScraperGenreTVShows.get_by_id(genre_data["id"])
            ScraperTVShowGenres.get_or_create(tvshow=tvshow, genre=genre)

        for lang_data in data["languages"]:
            ScraperTVShowLanguages.get_or_create(tvshow=tvshow, iso_639_1=lang_data["iso_639_1"])

        for network_data in data["networks"]:
            network = ScraperNetwork.from_data_dict(network_data)
            ScraperTVShowNetworks.get_or_create(tvshow=tvshow, network=network)

        for oc_data in data["origin_country"]:
            country = ScraperCountry.get(iso_3166_1=oc_data["iso_3166_1"])
            ScraperTVShowOriginCountry().get_or_create(tvshow=tvshow, country=country)

        for comp_data in data["production_companies"]:
            company = ScraperCompany.from_data_dict(comp_data)
            ScraperTVShowProductionCompanies.get_or_create(tvshow=tvshow, company=company)

        for country_data in data["production_countries"]:
            country = ScraperCountry.get(iso_3166_1=country_data["iso_3166_1"])
            ScraperTVShowProductionCountries.get_or_create(tvshow=tvshow, country=country)

        for season_data in data["seasons"]:
            ScraperTVShowSeason.from_data_dict(season_data)

        for spoken_data in data["spoken_languages"]:
            ScraperTVShowSpokenLanguages.get_or_create(
                tvshow=tvshow, iso_639_1=spoken_data["iso_639_1"]
            )

        if "credits" in data and "cast" in data["credits"]:
            for cast_data in data["credits"]["cast"]:
                ScraperTVShowCast.from_data_dict(cast_data)

        return ScraperTVShow.get_or_none(id=tmdb_id)

    @classmethod
    def get_tvshow_season_details(
        cls, tvshow_id: int, season: int, force_update: bool = False
    ) -> ScraperTVShowSeason:
        """returns the full tv show details"""

        if not force_update:
            if season_model := ScraperTVShowSeason.get_or_none(
                tvshow_id=tvshow_id, season_number=season
            ):
                return season_model

        data = cls.__get(f"/3/tv/{tvshow_id}/season/{season}")

        tvshow_model = ScraperTVShow.get_or_none(id=tvshow_id)
        if tvshow_model is None:
            tvshow_model = cls.get_tvshow_details(tvshow_id)
            return cls.get_tvshow_season_details(tvshow_id, season)

        season_model = ScraperTVShowSeason.from_data_dict(data)

        for episode_data in data["episodes"]:
            episode = ScraperTVShowEpisode.from_data_dict(episode_data, season_model)
            for guest_star_data in episode_data["guest_stars"]:
                ScraperTVShowGuestStars.from_data_dict(guest_star_data, episode)

        return ScraperTVShowSeason.get_or_none(id=data["id"])

    @classmethod
    def get_tvshow_episode_details(
        cls, tvshow_id: int, season: int, episode: int, force_update: bool = False
    ) -> ScraperTVShowEpisode:
        """returns the full tv show details"""

        if not force_update:
            if episode_model := ScraperTVShowEpisode.get_or_none(
                tvshow_id=tvshow_id, season_number=season, episode_number=episode
            ):
                return episode_model

        data = cls.__get(f"/3/tv/{tvshow_id}/season/{season}/episode/{episode}")

        season_model = ScraperTVShowSeason.get_or_none(tvshow_id=tvshow_id, season_number=season)
        if season_model is None:
            season_model = cls.get_tvshow_season_details(tvshow_id, season)
            return cls.get_tvshow_episode_details(tvshow_id, season, episode)

        episode = ScraperTVShowEpisode.from_data_dict(data, season_model)

        for guest_star_data in data["guest_stars"]:
            ScraperTVShowGuestStars.from_data_dict(guest_star_data, episode)

        return ScraperTVShowEpisode.get_or_none(id=data["id"])
