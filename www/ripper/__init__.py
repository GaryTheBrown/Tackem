'''Ripper Root pages'''
from libs.authenticator import Authentication
import cherrypy
from libs.html_template import HTMLTEMPLATE
from libs.html_system import HTMLSystem
from data.config import CONFIG
from libs.ripper import Ripper


class RipperRoot(HTMLTEMPLATE):
    '''ROOT OF PLUGINS WEBUI HERE'''
    @cherrypy.expose
    def index(self):
        '''index of Ripper'''
        Authentication.check_auth()
        return self._template(
            HTMLSystem.part(
                "pages/ripper_index",
                DRIVES=self.drives_data(True),
                ISOCOUNT=len(Ripper.isos),
                ISOTHREADLIMIT=CONFIG['ripper']['iso']['threadcount'].value
            )
        )

    def drive_data(self, drive_obj, drive_index, vertical=False):
        '''return html for Drive'''
        data = drive_obj.html_data(False)
        return HTMLSystem.part(
            "ripping/drives/itemvertical" if vertical else "ripping/drives/item",
            DRIVENUMBER=str(drive_index),
            LOCKED="" if data["traylock"] else "hidden",
            NAME=drive_obj.name,
            IMAGE=data["traystatus"],
            INFO=data["drivestatus"],
            RIPPINGDATAVISIBLE="" if data['ripping'] else "hidden",
            RIPPINGDATA=data["rippingdata"] if data['ripping'] else ""
        )

    def drives_data(self, vertical=False):
        '''returns the group of drives html'''
        html = ""
        for drive_index, drive_obj in enumerate(Ripper.drives):
            html += self.drive_data(drive_obj, drive_index , vertical)
        return html
