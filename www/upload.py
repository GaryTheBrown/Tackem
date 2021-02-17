'''Script For the Root Of The System'''
from libs.database.where import Where
from data.database.upload import UPLOAD_DB_INFO
from libs.database import Database
from libs.database.messages.select import SQLSelect
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
            UPLOAD_DB_INFO.name(),
            Where("key", key)
        )
        Database.call(msg)

        if isinstance(msg.return_data, list):
            raise cherrypy.HTTPError(status=403)

        filename = msg.return_data['filename']

        upload_folder = File.location(f"{CONFIG['webui']['uploadlocation'].value}{filename}")
        with open(upload_folder, 'wb') as file:
            shutil.copyfileobj(cherrypy.request.body, file)

        #TODO Do some magic here to check the Key in the upload Access DB and then put the file
        # where it needs to go from there

        # from msg.return_data['system'] and msg.return_data['link_id'] send the file to the correct
        # location so far only "audioISO" and "videoISO"
        return 'OK'
