"""Script For the Root Of The System"""
import os
import shutil

import cherrypy
from peewee import DoesNotExist

from data.config import CONFIG
from data.database.post_upload import PostUpload
from libs.file import File
from libs.ripper import Ripper


class Upload:
    """Root"""

    @cherrypy.expose()
    def index(self, key: str = None):
        """Handle non-multipart upload"""
        if key is None:
            raise cherrypy.HTTPError(status=403)

        try:
            info = PostUpload.do_select().where(PostUpload.key == key).get()
        except DoesNotExist:
            raise cherrypy.HTTPError(status=403)

        filename = info.filename
        upload_name = File.location(f"{CONFIG['webui']['uploadlocation'].value}{filename}")

        with open(upload_name, "wb") as file:
            shutil.copyfileobj(cherrypy.request.body, file)

        if os.path.getsize(upload_name) == info.filesize:
            system = info.system
            info.delete_instance()
            self.__call_next_system(filename, system)
            return "OK"
        return "FAILED"

    def __call_next_system(self, filename: str, system: str):
        """Sends command to the next system"""
        source_file = File.location(f"{CONFIG['webui']['uploadlocation'].value}{filename}")
        if system == "RIPPER_ISO":
            File.move(
                source_file,
                File.location(f"{CONFIG['ripper']['locations']['iso'].value}{filename}"),
            )
            Ripper.iso_add(filename)
            return
