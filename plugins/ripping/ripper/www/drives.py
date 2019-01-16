'''drives pages'''
import os
import cherrypy
from libs.html_template import HTMLTEMPLATE

class Drives(HTMLTEMPLATE):
    '''ROOT OF PLUGINS WEBUI HERE'''
    @cherrypy.expose
    def index(self):
        '''index of Drives'''
        index_page = ""
        for drive_index, drive in enumerate(self._system.get_drives()):
            index_page += self._drive_html(drive, drive_index)
        return self._template(index_page)

    @cherrypy.expose
    def single(self, index=None, data=None):
        '''index of Drives'''
        if index is None:
            return "FAILED No Index"
        try:
            index_int = int(index)
        except ValueError:
            return "Failed Not an Index"
        drives = self._system.get_drives()
        if index_int > len(drives):
            return "Failed Index Out Of Range"
        drive = self._system.get_drives()[index_int]
        if data is None:
            return self._drive_html(drive, index_int)
        return self.drive_data(drive, data)

    def drive_data(self, drive, data):
        '''returns the piece of data requested'''
        if data == "traystatus":
            tray_status = drive.get_tray_status()
            if tray_status == "empty":
                return "/ripping/ripper/static/images/empty.png"
            elif tray_status == "open":
                return "/ripping/ripper/static/images/open.png"
            elif tray_status == "reading":
                return "/ripping/ripper/static/images/reading.gif"
            elif tray_status == "loaded":
                disc_type = drive.get_disc_type()
                if disc_type == "none":
                    return "/ripping/ripper/static/images/reading.gif"
                elif disc_type == "audiocd":
                    return "/ripping/ripper/static/images/audiocd.png"
                elif disc_type == "dvd":
                    return "/ripping/ripper/static/images/dvd.png"
                elif disc_type == "bluray":
                    return "/ripping/ripper/static/images/bluray.png"
        elif data == "drivestatus":
            return drive.get_drive_status()
        elif data == "traylock":
            return str(drive.get_tray_locked())

    def _drive_html(self, drive, drive_index):
        '''return html for Drive'''
        drive_html = str(open(os.path.dirname(__file__) + '/html/drive.html', "r").read())
        locked_html = ""
        if not drive.get_tray_locked():
            locked_html = 'style="display:none"'
        name_html = ""
        cfg_name = drive.get_cfg_name()
        name = self._lconfig['drives'][cfg_name]['name']
        if name != "":
            name_html += name + "("
        name_html += drive.get_device()
        if name != "":
            name_html += ")"
        drive_html = drive_html.replace("%%DRIVENUMBER%%", str(drive_index))
        drive_html = drive_html.replace("%%IMAGE%%", self.drive_data(drive, "traystatus"))
        drive_html = drive_html.replace("%%LOCKED%%", locked_html)
        drive_html = drive_html.replace("%%NAME%%", name_html)
        drive_html = drive_html.replace("%%INFO%%", self.drive_data(drive, "drivestatus"))
        return drive_html
