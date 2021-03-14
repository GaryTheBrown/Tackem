"""Script For the Root Of The System"""
from libs.ripper import Ripper
from data.database.ripper import AUDIO_INFO_DB, VIDEO_INFO_DB
from libs.database.messages.delete import SQLDelete
import os
from libs.database.where import Where
from data.database.system import UPLOAD_DB
from libs.database import Database
from libs.database.messages import SQLSelect
from data.config import CONFIG
import cherrypy
import shutil
from libs.html_template import HTMLTEMPLATE
from libs.file import File


class Upload(HTMLTEMPLATE):
    """Root"""

    @cherrypy.expose()
    def index(self, key: str = None):
        """Handle non-multipart upload"""
        if key is None:
            raise cherrypy.HTTPError(status=403)

        msg = SQLSelect(UPLOAD_DB, Where("key", key))
        Database.call(msg)

        if isinstance(msg.return_data, list):
            raise cherrypy.HTTPError(status=403)

        filename = msg.return_data["filename"]
        upload_name = File.location(
            f"{CONFIG['webui']['uploadlocation'].value}{filename}"
        )

        with open(upload_name, "wb") as file:
            shutil.copyfileobj(cherrypy.request.body, file)

        if os.path.getsize(upload_name) == msg.return_data["filesize"]:
            Database.call(SQLDelete(UPLOAD_DB, Where("id", msg.return_data["id"])))
            self.__call_next_system(filename, msg.return_data["system"])
            return "OK"
        return "FAILED"

    def __call_next_system(self, filename: str, system: str):
        """Sends command to the next system"""
        source_file = File.location(
            f"{CONFIG['webui']['uploadlocation'].value}{filename}"
        )
        if system == "RIPPER_ISO_AUDIO":
            File.move(
                source_file,
                File.location(
                    f"{CONFIG['ripper']['locations']['audioiso'].value}{filename}"
                ),
            )
            Ripper.iso_add(filename, AUDIO_INFO_DB)
            return
        if system == "RIPPER_ISO_VIDEO":
            File.move(
                source_file,
                File.location(
                    f"{CONFIG['ripper']['locations']['videoiso'].value}{filename}"
                ),
            )
            Ripper.iso_add(filename, VIDEO_INFO_DB)
            return
