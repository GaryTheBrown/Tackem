"""SCRAPER ROOT API"""
import cherrypy

from api.base import APIBase
from api.e404 import API404
from api.scraper.search_imdbid import APIScraperIMDBID
from api.scraper.search_movie import APIScraperSearchMovie
from api.scraper.search_tmdbid import APIScraperTMDBID
from api.scraper.search_tv import APIScraperSearchTV
from api.scraper.search_tvdbid import APIScraperTVDBID


@cherrypy.expose
class APIScraper(APIBase):
    """ROOT API"""

    def _cp_dispatch(self, vpath):
        """cp dispatcher overwrite"""
        if len(vpath) == 0:
            return self

        section = vpath.pop(0).lower()

        if section == "searchmovie":
            return APIScraperSearchMovie()
        if section == "searchtv":
            return APIScraperSearchTV()
        if section == "imdbid":
            return APIScraperIMDBID()
        if section == "tmdbid":
            return APIScraperTMDBID()
        if section == "tvdbid":
            return APIScraperTVDBID()
        return API404()
