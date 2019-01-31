'''Scraper for Ripper System'''
import json
import os
import cherrypy
from libs import html_parts as ghtml_parts
from libs.data.languages import Languages
from .scraper_base import Scraper
from . import html_parts

class ScraperRipper(Scraper):
    '''Scraper System Here'''

    @cherrypy.expose
    def index(self):
        '''index of scraper'''
        return "RUNNING"

    @cherrypy.expose
    def javascript(self):
        '''index of scraper'''
        java_file = str(open(os.path.dirname(__file__) + "/javascript/ripper.js", "r").read())
        return java_file.replace("%%BASEURL%%", self._config['webui']['baseurl'])

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def searchmovie(self, query, page=1, year=None):
        '''search for a movie by name (and Year)'''
        return self._search_for_movie(query, page, year)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def findmovie(self, imdb_id):
        '''search for a movie by imdb id'''
        return self._search_by_imdb_id(imdb_id)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getmovie(self, movie_id):
        '''get movie by TMDB id'''
        return self._get_movie_details(movie_id)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def searchtvshow(self, query, page=1):
        '''search for a tv show'''
        return self._search_for_tvshow(query, page)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def findtvshow(self, tvdb_id):
        '''search for a tv show by tvdb id'''
        return self._search_by_tvdb_id(tvdb_id)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def gettvshow(self, tvshow_id):
        '''get tv show by TMDB id'''
        return self._get_tvshow_details(tvshow_id)

#################
##MOVIE SECTION##
#################
    def _search_for_movie(self, query, page=1, year=None):
        '''searches for a movie getting all options'''
        data = self.search_for_movie(query, page, year)

        if data['success'] is False:
            return json.dumps(data)
        if int(data['response']['total_results']) == 1:
            return self._show_single_movie_item(data['response']['results'][0])

        response = data['response']
        pagination = "Pages:"
        if int(page) > 1:
            pagination += html_parts.movie_page_link(query, int(page)-1, year, "<<")
        for count in range(1, response['total_pages'] + 1):
            if count == int(page):
                pagination += "&nbsp" + str(page) + "&nbsp"
            else:
                pagination += html_parts.movie_page_link(query, count, year)
        if int(page) < response['total_pages']:
            pagination += html_parts.movie_page_link(query, int(page)+1, year, ">>")

        #items on this page
        total_results = response['total_results']
        low_count = (response['page'] - 1) * 20
        if total_results > 20 and total_results + 20 < response['page'] * 20:
            max_count = response['page'] * 20
        else:
            max_count = total_results
        page_range = str(low_count) + " to " + str(max_count) + " of " + str(total_results)

        #make the page of data for the modal
        accordian_name = "movie_list"
        accordian_cards = ""
        for index, item in enumerate(response['results']):
            header = item['title']
            if item['release_date'] != "":
                header += " (" + item['release_date'][:4] + ")"
            button = ghtml_parts.input_button("CHOOSE", "PopulateMovie(" + str(item['id']) + ");")
            full_original_language = Languages().get_name_from_2(item['original_language'])
            body = html_parts.search_info(item['title'], item['original_title'],
                                          full_original_language, item['overview'],
                                          item['release_date'], item['poster_path'],
                                          self._image_config['secure_base_url'],
                                          self._image_config['poster_sizes'][2])
            accordian_cards += ghtml_parts.accordian_card(accordian_name, index, header,
                                                          button, body)
        body = ghtml_parts.accordian(accordian_name, accordian_cards)
        return json.dumps({
            'success': True,
            'total_results': total_results,
            'header': 'Search Results "' + query + '" ' + page_range,
            'body': body,
            'footer': pagination
        })

    def _search_by_imdb_id(self, imdb_id):
        '''searches by the IMDB ID'''
        data = self.search_by_imdb_id(imdb_id)
        if data['success'] is False:
            return json.dumps(data)
        return self._show_single_movie_item(data['response']['movie_results'][0])

    def _show_single_movie_item(self, item):
        '''using the info shows a single item and asks if correct'''
        header = item['title']
        if item['release_date'] != "":
            header += " (" + item['release_date'][:4] + ")"
        full_original_language = Languages().get_name_from_2(item['original_language'])
        body = html_parts.search_info(item['title'], item['original_title'],
                                      full_original_language, item['overview'],
                                      item['release_date'], item['poster_path'],
                                      self._image_config['secure_base_url'],
                                      self._image_config['poster_sizes'][2])
        yes_button = ghtml_parts.input_button("Yes", "PopulateMovie(" + str(item['id']) + ");")
        no_button = ghtml_parts.input_button("No", "ClearModel();")
        footer = html_parts.yes_no_footer(yes_button, no_button)
        return json.dumps({
            'success': True,
            'header': header,
            'body': body,
            'footer': footer
        })

    def _get_movie_details(self, movie_id):
        '''returns the full movie details'''
        return json.dumps(self.get_movie_details(movie_id))

##################
##TVSHOW SECTION##
##################
    def _search_for_tvshow(self, query, page=1):
        '''searches for a movie getting all options'''
        data = self.search_for_tvshow(query, page)
        if data['success'] is False:
            return json.dumps(data)
        if int(data['response']['total_results']) == 1:
            return self._show_single_tvshow_item(data['response']['results'][0])

        response = data['response']
        pagination = "Pages:"
        if int(page) > 1:
            pagination += html_parts.tvshow_page_link(query, int(page)-1, "<<")
        for count in range(1, response['total_pages'] + 1):
            if count == int(page):
                pagination += "&nbsp" + str(page) + "&nbsp"
            else:
                pagination += html_parts.tvshow_page_link(query, count)
        if int(page) < response['total_pages']:
            pagination += html_parts.tvshow_page_link(query, int(page)+1, ">>")

        #items on this page
        total_results = response['total_results']
        low_count = (response['page'] - 1) * 20
        if total_results > 20 and total_results + 20 < response['page'] * 20:
            max_count = response['page'] * 20
        else:
            max_count = total_results
        page_range = str(low_count) + " to " + str(max_count) + " of " + str(total_results)

        #make the page of data for the modal
        accordian_name = "tvshow_list"
        accordian_cards = ""
        for index, item in enumerate(response['results']):
            header = item['name']
            button = ghtml_parts.input_button("CHOOSE", "PopulateTVShow(" + str(item['id']) + ");")
            full_original_language = Languages().get_name_from_2(item['original_language'])
            body = html_parts.search_info(item['name'], item['original_name'],
                                          full_original_language, item['overview'],
                                          item['first_air_date'], item['poster_path'],
                                          self._image_config['secure_base_url'],
                                          self._image_config['poster_sizes'][2])
            accordian_cards += ghtml_parts.accordian_card(accordian_name, index, header,
                                                          button, body)
        body = ghtml_parts.accordian(accordian_name, accordian_cards)
        return json.dumps({
            'success': True,
            'total_results': total_results,
            'header': 'Search Results "' + query + '" ' + page_range,
            'body': body,
            'footer': pagination
        })

    def _search_by_tvdb_id(self, imdb_id):
        '''searches by the TVDB ID'''
        data = self.search_by_tvdb_id(imdb_id)
        if data['success'] is False:
            return json.dumps(data)
        return self._show_single_tvshow_item(data['response']['tv_results'][0])

    def _show_single_tvshow_item(self, item):
        '''using the info shows a single item and asks if correct'''
        header = item['name']
        full_original_language = Languages().get_name_from_2(item['original_language'])
        body = html_parts.search_info(item['name'], item['original_name'],
                                      full_original_language, item['overview'],
                                      item['first_air_date'], item['poster_path'],
                                      self._image_config['secure_base_url'],
                                      self._image_config['poster_sizes'][2])
        yes_button = ghtml_parts.input_button("Yes", "PopulateTVShow(" + str(item['id']) + ");")
        no_button = ghtml_parts.input_button("No", "ClearModel();")
        footer = html_parts.yes_no_footer(yes_button, no_button)
        return json.dumps({
            'success': True,
            'header': header,
            'body': body,
            'footer': footer
        })

    def _get_tvshow_details(self, tvshow_id):
        '''returns the full tv show details'''
        return json.dumps(self.get_tvshow_details(tvshow_id))
