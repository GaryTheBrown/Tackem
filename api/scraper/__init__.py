"""SCRAPER ROOT API"""
import cherrypy

from api.base import APIBase
from api.e404 import API404
from api.scraper.movie_imdbid import APIScraperMovieIMDBID
from api.scraper.movie_search import APIScraperMovieSearch
from api.scraper.movie_tmdbid import APIScraperMovieTMDBID
from api.scraper.tv_imdbid import APIScraperTVIMDBID
from api.scraper.tv_search import APIScraperTVSearch
from api.scraper.tv_tmdbid import APIScraperTVTMDBID
from api.scraper.tv_tvdbid import APIScraperTVTVDBID


@cherrypy.expose
class APIScraper(APIBase):
    """ROOT API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""
        if len(vpath) == 0:
            return self

        section = vpath.pop(0).lower()

        if section == "moviesearch":
            return APIScraperMovieSearch()
        if section == "moviesearchimdbid":
            return APIScraperMovieIMDBID()
        if section == "moviesearchtmdbid":
            return APIScraperMovieTMDBID()
        if section == "tvsearch":
            return APIScraperTVSearch()
        if section == "tvsearchtvdbid":
            return APIScraperTVTVDBID()
        if section == "tvsearchimdbid":
            return APIScraperTVIMDBID()
        if section == "tvsearchtmdbid":
            return APIScraperTVTMDBID()
        if section == "docsearch":
            return APIScraperMovieSearch()
        if section == "docsearchimdbid":
            return APIScraperMovieSearch()
        if section == "docsearchtvdbid":
            return APIScraperMovieSearch()
        if section == "docsearchtmdbid":
            return APIScraperMovieSearch()
        return API404()
