'''Script For the Root Of The System'''
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
    '''Root'''

    @cherrypy.expose()
    def index(self, key: str = None):
        '''Handle non-multipart upload'''
        if key is None:
            raise cherrypy.HTTPError(status=403)

        msg = SQLSelect(
            UPLOAD_DB.name(),
            Where("key", key)
        )
        Database.call(msg)

        if isinstance(msg.return_data, list):
            raise cherrypy.HTTPError(status=403)

        filename = msg.return_data['filename']

        upload_name = File.location(f"{CONFIG['webui']['uploadlocation'].value}{filename}")
        with open(upload_name, 'wb') as file:
            shutil.copyfileobj(cherrypy.request.body, file)

        if os.path.getsize(upload_name) == msg.return_data['filesize']:
            Database.call(SQLDelete(UPLOAD_DB.name(), Where("id", self._db_data['id'])))
            return 'OK'
        return "FAILED"
