'''WEBUI FOR PLUGIN'''
import json
import cherrypy
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.htmltemplate import HTMLTEMPLATE

LAYOUT = {}
def cfg(config):
    '''generate the cherrypy conf'''
    temp_config = config['plugins']['ripping']['ripper']['locations']
    temp_video_location = temp_config['videoripping']
    if temp_config['videoripping'] != "/":
        temp_video_location = PROGRAMCONFIGLOCATION + temp_config['videoripping']
    temp_audio_location = temp_config['audioripping']
    if temp_config['audioripping'] != "/":
        temp_audio_location = PROGRAMCONFIGLOCATION + temp_config['audioripping']

    conf_root = {
        '/tempvideo': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': temp_video_location
        },
        '/tempaudio': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': temp_audio_location
        }
    }

    return conf_root

class Root(HTMLTEMPLATE):
    '''ROOT OF PLUGINS WEBUI HERE'''
    @cherrypy.expose
    def index(self):
        '''index of plugin'''
        index_page = self._name + " ROOT<br>"
        index_page += json.dumps(self._config['plugins']['ripping']['ripper'])
        return self._template(index_page)
