'''WEBUI FOR PLUGIN'''
import json
import cherrypy
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.html_template import HTMLTEMPLATE

LAYOUT = {}
def mounts(plugin_base_url, key, systems, plugins, config):
    '''where the system creates the cherrypy mounts'''
    cherrypy.tree.mount(Root(key, systems, plugins, config, "Ripper"),
                        plugin_base_url,
                        cfg(config))

def cfg(config):
    '''generate the cherrypy conf'''
    temp_config = config['plugins']['ripping']['ripper']['locations']
    temp_video_location = temp_config['videoripping']
    if temp_config['videoripping'][0] != "/":
        temp_video_location = PROGRAMCONFIGLOCATION + temp_config['videoripping']
    temp_audio_location = temp_config['audioripping']
    if temp_config['audioripping'][0] != "/":
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
        index_page = ""
        for drive in self._system.get_drives():
            index_page += "Name:" + drive.get_device() + "<br>"
            index_page += "thread running:" + str(drive.get_thread_run()) + "<br>"
            index_page += "tray status:" + str(drive.get_tray_status()) + "<br>"
            index_page += "tray locked:" + str(drive.get_tray_locked()) + "<br>"
            index_page += "disc type:" + str(drive.get_disc_type()) + "<br>"

        index_page += "<br>"
        index_page += "<br>"
        index_page += json.dumps(self._lconfig)
        index_page += "<br>"
        index_page += "<br>"
        index_page += json.dumps(self._plugin.SETTINGS)
        return self._template(index_page)
