'''Labeler pages'''
import json
from glob import glob
import cherrypy
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.html_template import HTMLTEMPLATE
from . import html_parts
from ..data import disc_type
from ..ffprobe import FFprobe

class Labeler(HTMLTEMPLATE):
    '''LABELER OF PLUGINS WEBUI HERE'''
    @cherrypy.expose
    def index(self):
        '''index of plugin'''
        root_html = html_parts.get_page("labeler/index", self._system)
        data = self._system.get_labeler().get_data("WWW" + cherrypy.request.remote.ip)
        labeler_html = html_parts.labeler_items(data, self._baseurl, False)
        root_html = root_html.replace("%%LABELERS%%", labeler_html)
        return self._template(root_html)

    @cherrypy.expose
    def single(self, index=None, vertical=True):
        '''get single labeler item'''
        if index is None:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        try:
            index_int = int(index)
        except ValueError:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        data = self._system.get_labeler().get_data_by_id("WWW" + cherrypy.request.remote.ip,
                                                         index_int)
        if data is False:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        if isinstance(vertical, str):
            vertical = False
        return html_parts.labeler_item(data, self._baseurl, vertical)

    @cherrypy.expose
    def getids(self):
        '''index of Drives'''
        return json.dumps(self._system.get_labeler().get_ids("WWW" + cherrypy.request.remote.ip))

    @cherrypy.expose
    def edit(self, index=None):
        '''edit the data page'''
        if index is None:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        try:
            index_int = int(index)
        except ValueError:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        data = self._system.get_labeler().get_data_by_id("WWW" + cherrypy.request.remote.ip,
                                                         index_int)
        if data is False:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")

        edit_html = html_parts.get_page("labeler/edit/edit", self._system)
        visibility = ""
        if data['rip_data'] is None:
            disc_type_html = self._edit_disc_type_work(data, 'change')
            visibility = 'style="display:none;"'
        else:
            rip_data = disc_type.make_disc_type(json.loads(data['rip_data']))
            disc_type_html = self._edit_disc_type_work(data, rip_data.disc_type())

        edit_html = edit_html.replace("%%DISCTYPESECTION%%", disc_type_html)
        edit_html = edit_html.replace("%%VISIBILITY%%", visibility)
        edit_html = edit_html.replace("%%DISCID%%", str(data['id']))

        #tracks here
        file_location = self._config['locations']['videoripping']
        if file_location[0] != "/":
            file_location = PROGRAMCONFIGLOCATION + self._config['locations']['videoripping']
        file_dir = file_location + str(data['id']) + "/"
        track_files = glob(file_dir + "*.mkv")
        track_files.sort()
        tracks_html = ""
        ffprobe_location = self._config['converter']['ffprobelocation']
        for track_index, track_file in enumerate(track_files):
            probe_info = FFprobe(ffprobe_location, track_file)
            tracks_html += html_parts.labeler_tracktype_section(data['id'], track_index, probe_info)
            #get main track data
            #grab individual track data to go inside of each track section
        edit_html = edit_html.replace("%%TRACKS%%", tracks_html)
        return self._template(edit_html)

    @cherrypy.expose
    def editdisctype(self, index=None, disc_type_code=None):
        '''gets the disc type html'''
        if index is None:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        try:
            index_int = int(index)
        except ValueError:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        data = self._system.get_labeler().get_data_by_id("WWW" + cherrypy.request.remote.ip,
                                                         index_int)
        if data is False:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        if disc_type_code is None:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        return self._edit_disc_type_work(data, disc_type_code)

    def _edit_disc_type_work(self, data, disc_type_code):
        '''work shared between two functions'''
        if disc_type_code.lower() == "change":
            disc_type_html = html_parts.labeler_disctype_start()
            rip_data = None
        else:
            if isinstance(data['rip_data'], str):
                rip_data = disc_type.make_disc_type(json.loads(data['rip_data']))
            elif isinstance(data['rip_data'], dict):
                rip_data = disc_type.make_disc_type(data['rip_data'])
            else:
                rip_data = data['rip_data']
            if rip_data is None:
                label = data['label']
                if disc_type_code.lower() == "movie":
                    rip_data = disc_type.MovieDiscType("", "", 0, "", None)
                elif disc_type_code.lower() == "tv show":
                    rip_data = disc_type.TVShowDiscType("", "", "", None)
                else:
                    return self._redirect(self._baseurl + "ripping/ripper/labeler/")
            else:
                label = rip_data.name()
            disc_type_html = html_parts.labeler_disctype_template(label, disc_type_code,
                                                                  rip_data)

        if rip_data is not None and rip_data.name() != "":
            disc_type_html = disc_type_html.replace("%%DISCLABEL%%", rip_data.name())
        else:
            disc_type_html = disc_type_html.replace("%%DISCLABEL%%", data['label'])
        disc_type_html = disc_type_html.replace("%%DISCID%%", str(data['id']))
        return disc_type_html

    # @cherrypy.expose
    # def edittracktype(self, disc_index=None, track_index=None, track_type_code=None):
    #     '''gets the disc type html'''
    #     if disc_index is None or track_index is None:
    #         return self._redirect(self._baseurl + "ripping/ripper/labeler/")
    #     try:
    #         disc_index_int = int(disc_index)
    #         track_index_int = int(track_index)
    #     except ValueError:
    #         return self._redirect(self._baseurl + "ripping/ripper/labeler/")
    #     data = self._system.get_labeler().get_data_by_id("WWW" + cherrypy.request.remote.ip,
    #                                                      disc_index_int)
    #     if data is False:
    #         return self._redirect(self._baseurl + "ripping/ripper/labeler/")
    #     if track_type_code is None:
    #         return self._redirect(self._baseurl + "ripping/ripper/labeler/")
    #     return self._edit_track_type_work(data, track_index_int, track_type_code)

    # def _edit_track_type_work(self, data, track_index, track_type_code):
    #     '''work shared between two functions'''
    #     if track_type_code.lower() == "change":
    #         track_type_html = html_parts.labeler_tracktype_start()
    #         rip_data = None
    #     else:
    #         if isinstance(data['rip_data'], str):
    #             rip_data = disc_type.make_disc_type(json.loads(data['rip_data']))
    #         elif isinstance(data['rip_data'], dict):
    #             rip_data = disc_type.make_disc_type(data['rip_data'])
    #         else:
    #             rip_data = data['rip_data']
    #         tracks = rip_data.tracks()
    #         if not tracks:
    #             return self._redirect(self._baseurl + "ripping/ripper/labeler/")




    @cherrypy.expose
    def editsave(self, **kwargs):
        '''saves the disc type'''
        #first sort the tracks here
        rip_data = disc_type.save_html_to_disc_type(kwargs)

        #if complete text box ticked send to next system
        finished = False
        self._system.get_labeler().set_data("WWW" + cherrypy.request.remote.ip, kwargs['discid'],
                                            rip_data, finished)

        return self._redirect(self._baseurl + "ripping/ripper/labeler/")
