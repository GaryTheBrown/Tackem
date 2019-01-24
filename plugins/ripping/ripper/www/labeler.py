'''Labeler pages'''
import datetime
import json
from glob import glob
import cherrypy
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.html_template import HTMLTEMPLATE
from . import html_parts
from ..data import disc_type
from ..data import video_track_type
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
            rip_data = json.loads(data['rip_data'])
            disc_info = disc_type.make_disc_type(rip_data)
            disc_type_html = self._edit_disc_type_work(data, disc_info.disc_type())

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
        for track_index, track_file in enumerate(track_files):
            track_data = None
            if "tracks" in rip_data and isinstance(rip_data['tracks'], list):
                if len(rip_data['tracks']) >= track_index:
                    track_data = rip_data['tracks'][track_index]
            tracks_html += self._tracktype_section(data['id'], track_index, track_file, track_data)
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
        if disc_type_code == "change":
            self._system.get_labeler().clear_rip_data("WWW" + cherrypy.request.remote.ip, index_int)
        return self._edit_disc_type_work(data, disc_type_code)

    def _edit_disc_type_work(self, data, disc_type_code):
        '''work shared between two functions'''
        if disc_type_code == "change":
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
                rip_data = disc_type.make_blank_disc_type(disc_type_code)
                if rip_data is None:
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

    def _tracktype_section(self, disc_index, track_index, track_file, track_data=None):
        '''labeler disc type templated section'''
        probe_info = FFprobe(self._config['converter']['ffprobelocation'], track_file)
        stream_counts = probe_info.stream_type_count()
        format_info = probe_info.get_format_info()
        length = str(datetime.timedelta(seconds=int(format_info["duration"].split(".")[0])))
        video_url = "/".join(cherrypy.url().split("/")[:-3]) + "/tempvideo/"
        video_url += str(disc_index) + "/" + str(track_index).zfill(2) + ".mkv"
        if 'audio' in stream_counts:
            audio_count = str(stream_counts['audio'])
        else:
            audio_count = "0"
        if 'subtitle' in stream_counts:
            subtitle_count = str(stream_counts['subtitle'])
        else:
            subtitle_count = "0"
        if probe_info.has_chapters():
            has_chapters = "Yes"
        else:
            has_chapters = "No"

        panel_head_html = html_parts.get_page("labeler/edit/tracktype/panelname")
        panel_head_html = panel_head_html.replace("%%TRACKLENGTH%%", length)
        panel_head_html = panel_head_html.replace("%%TRACKURL%%", video_url)
        panel_head_html = panel_head_html.replace("%%AUDIOCOUNT%%", audio_count)
        panel_head_html = panel_head_html.replace("%%SUBTITLECOUNT%%", subtitle_count)
        panel_head_html = panel_head_html.replace("%%HASCHAPTERS%%", has_chapters)
        if track_data is None:
            section_html = html_parts.labeler_tracktype_start()
        else:
            section_html = self._edit_track_type_work(track_data, track_data['video_type'])

        track_panel = html_parts.panel(panel_head_html, "track_" + str(track_index), section_html)
        track_panel = track_panel.replace("%%TRACKINDEX%%", str(track_index))
        return track_panel

    @cherrypy.expose
    def edittracktype(self, disc_index=None, track_index=None, track_type_code=None):
        '''gets the disc type html'''
        if disc_index is None or track_index is None:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        try:
            disc_index_int = int(disc_index)
            track_index_int = int(track_index)
        except ValueError:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        data = self._system.get_labeler().get_data_by_id("WWW" + cherrypy.request.remote.ip,
                                                         disc_index_int)
        if data is False:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        if track_type_code is None:
            return self._redirect(self._baseurl + "ripping/ripper/labeler/")
        rip_data = json.loads(data['rip_data'])
        track_data = None
        if "tracks" in rip_data and isinstance(rip_data["tracks"], list):
            if len(rip_data["tracks"]) >= track_index_int:
                track_data = rip_data["tracks"][track_index_int]
        if track_data and track_type_code == "change":
            self._system.get_labeler().clear_rip_track_data("WWW" + cherrypy.request.remote.ip,
                                                            disc_index_int, track_index_int)
        track_type_html = self._edit_track_type_work(track_data, track_type_code)
        return track_type_html.replace("%%TRACKINDEX%%", str(track_index))

    def _edit_track_type_work(self, track_data, track_type_code):
        '''work shared between two functions'''
        if track_type_code == "change":
            return html_parts.labeler_tracktype_start()
        elif track_data is None:
            track_data = video_track_type.make_blank_track_type(track_type_code)
            return track_data.get_edit_panel()
        return video_track_type.make_track_type(track_data).get_edit_panel()

    @cherrypy.expose
    def editsave(self, **kwargs):
        '''saves the disc type'''
        #first sort the tracks here
        file_location = self._config['locations']['videoripping']
        if file_location[0] != "/":
            file_location = PROGRAMCONFIGLOCATION + self._config['locations']['videoripping']
        file_dir = file_location + str(kwargs['discid']) + "/"
        data = {}
        data['tracks'] = [None] * len(glob(file_dir + "*.mkv"))
        for item in kwargs:
            array = item.split("_")
            if len(array) <= 2:
                if item != "complete":
                    data[item] = kwargs[item]
            elif array[0] == "track":
                if not isinstance(data['tracks'][int(array[1])], dict):
                    data['tracks'][int(array[1])] = {}
                if array != "section":
                    if len(array) == 3:
                        data['tracks'][int(array[1])][array[2]] = kwargs[item]
                    elif len(array) == 4:
                        data['tracks'][int(array[1])][array[2] + "_" + array[3]] = kwargs[item]
                #section stuff here
        rip_data = disc_type.save_html_to_disc_type(data)
        #if complete text box ticked send to next system
        finished = "complete" in kwargs
        self._system.get_labeler().set_data("WWW" + cherrypy.request.remote.ip, kwargs['discid'],
                                            rip_data, finished)
        return self._redirect(self._baseurl + "ripping/ripper/labeler/")
