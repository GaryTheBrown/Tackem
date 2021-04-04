"""SCRAPER ROOT API"""
import cherrypy

from api.base import APIBase
from api.e404 import API404
from api.scraper.movie_search import APIScraperMovieSearch


@cherrypy.expose
class APIScraper(APIBase):
    """ROOT API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""
        if len(vpath) == 0:
            return self

        section = vpath.pop(0)

        if section == "movieSearch":
            return APIScraperMovieSearch()
        if section == "movieSearchIMDBid":
            return APIScraperMovieSearch()
        if section == "movieSearchTMDBid":
            return APIScraperMovieSearch()
        if section == "tvSearch":
            return APIScraperMovieSearch()
        if section == "tvSearchTVDBid":
            return APIScraperMovieSearch()
        if section == "tvSearchTMDBid":
            return APIScraperMovieSearch()
        if section == "docSearch":
            return APIScraperMovieSearch()
        if section == "docSearchIMDBid":
            return APIScraperMovieSearch()
        if section == "docSearchTVDBid":
            return APIScraperMovieSearch()
        if section == "docSearchTMDBid":
            return APIScraperMovieSearch()
        return API404()
