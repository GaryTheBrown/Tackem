'''Scraper System'''
import http.client
import json
import os
import cherrypy
from libs import html_parts as ghtml_parts
from . import html_parts

class Scraper():
    '''Scraper System Here'''

    def __init__(self, config):
        self._config = config
        self._apikey = config['scraper']['apikey']
        self._language = config['scraper']['language']
        self._include_adult = config['scraper']['includeadult']
        self._conn = http.client.HTTPSConnection("api.themoviedb.org")
        self._image_config = self._configuration()

    @cherrypy.expose
    def index(self):
        '''index of scraper'''
        return "RUNNING"

    @cherrypy.expose
    def javascript(self):
        '''index of scraper'''
        java_file = str(open(os.path.dirname(__file__) + "/javascript.js", "r").read())
        return java_file.replace("%%BASEURL%%", self._config['webui']['baseurl'])

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def searchmovie(self, query, page=1, year=None):
        '''search for a movie'''
        return self._search_for_movie(query, page, year)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def findmovie(self, imdb_id):
        '''search for a movie by imdb id'''
        return self._search_by_imdb_id(imdb_id)

#############
##SHORTCUTS##
#############
    def _base(self, adult=True, language=True):
        '''creates the base command keys'''
        base = "api_key=" + self._apikey
        if adult:
            base += "&include_adult=" + str(self._include_adult).lower()
        if language:
            base += "&language=" + self._language
        return base

    def _fail_print(self, status, reason):
        '''message returned when the scraper failed'''
        return "Search Failed\nStatus: " + status + "\nReason: " + reason + "\n"

############
##COMMANDS##
############
    def _configuration(self):
        '''config section for startup getting info mainly image urls'''
        command = "/3/configuration?" + self._base(False, False)
        data = self._get_request(command)
        if data['success'] is False:
            print("ERROR IN SCRAPER STARTUP:", self._fail_print(data['status'], data['reason']))
            return None
        return data['response']['images']

    def _search_for_movie(self, query, page=1, year=None):
        '''searches for a movie getting all options'''
        query_to_go = query.replace(" ", "+")
        command = "/3/search/movie?" + self._base() + "&page=" + str(page)
        command += "&query=" + query_to_go
        if year:
            command += "&year=" + str(year)

        data = self._get_request(command)
        if data['success'] is False:
            return json.dumps(data)
        print(data['response']['total_results'], int(data['response']['total_results']) == 1)
        if int(data['response']['total_results']) == 1:
            return self._show_single_item(data['response']['results'][0])

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
            body = html_parts.movie_info(item['title'], item['original_title'],
                                         item['original_language'], item['overview'],
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
            'footer': pagination #TODO FIX THIS NOT SHOWING
        })

    def _search_by_imdb_id(self, imdb_id):
        '''searches by the IMDB ID'''
        command = "/3/find/" + str(imdb_id) + "?" + self._base(adult=False)
        command += "&external_source=imdb_id"
        data = self._get_request(command)
        if data['success'] is False:
            return json.dumps(data)
        return self._show_single_item(data['response']['movie_results'][0])

    def _show_single_item(self, item):
        '''using the info shows a single item and asks if correct'''
        header = item['title']
        if item['release_date'] != "":
            header += " (" + item['release_date'][:4] + ")"
        body = html_parts.movie_info(item['title'], item['original_title'],
                                     item['original_language'], item['overview'],
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

        command = "/3/movie/" + str(movie_id) + "/?" + self._base(adult=False)

        data = self._get_request(command)
        if data['success'] is False:
            return json.dumps(data)

        #TODO what do I do with all this data? see temp files

##############
##HTTP Calls##
##############
    def _get_request(self, command):
        '''do a get request'''
        self._conn.request("GET", command)
        response = self._conn.getresponse()
        return_data = {
            "status":int(response.status),
            "reason":response.reason
        }
        success = int(response.status) == 200 and response.reason == "OK"
        return_data['success'] = success
        if success:
            return_data['response'] = json.loads(response.read().decode("utf-8"))
        return return_data


# payload = "{}"
# conn.request("GET", , payload)
