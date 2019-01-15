'''drives pages'''
import os
import cherrypy
from libs.html_template import HTMLTEMPLATE

class Drives(HTMLTEMPLATE):
    '''ROOT OF PLUGINS WEBUI HERE'''
    @cherrypy.expose
    def index(self):
        '''index of Drives'''
        index_page = "<h1>Drives</h1><br>"
        for drive in self._system.get_drives():
            index_page += self._drive_html(drive)
        return self._template(index_page)

    @cherrypy.expose
    def single(self, index=None):
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
        index_page = "<h1>Drive " + str(index) + "</h1><br>"
        index_page += self._drive_html(self._system.get_drives()[index_int])

        return index_page

    def _drive_html(self, drive):
        '''index of Drives'''
        drive_html = str(open(os.path.dirname(__file__) + '/html/drive.html', "r").read())
        tray_status = drive.get_tray_status()
        if tray_status == "empty":
            image_html = "/ripping/ripper/static/images/empty.png"
        elif tray_status == "open":
            image_html = "/ripping/ripper/static/images/open.png"
        elif tray_status == "reading":
            image_html = "/ripping/ripper/static/images/reading.gif"
        elif tray_status == "loaded":
            disc_type = drive.get_disc_type()
            if disc_type == "audiocd":
                image_html = "/ripping/ripper/static/images/audiocd.png"
            elif disc_type == "dvd":
                image_html = "/ripping/ripper/static/images/dvd.png"
            elif disc_type == "bluray":
                image_html = "/ripping/ripper/static/images/bluray.png"

        drive_html = drive_html.replace("%%IMAGE%%", image_html)
        drive_html += "Name:" + drive.get_device() + "<br>"
        drive_html += "tray locked:" + str(drive.get_tray_locked()).title() + "<br>"
        drive_html += "disc status:" + str(drive.get_drive_status()).title() + "<br>"
        return drive_html
