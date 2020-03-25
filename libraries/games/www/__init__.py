'''WEBUI FOR PLUGIN'''
import cherrypy
from libs.authenticator import AUTHENTICATION
from libs.html_template import HTMLTEMPLATE
from system.plugin import TackemSystemPlugin
from config_data import CONFIG

LAYOUT = {}


def mounts(key, instance_name=None):
    '''where the system creates the cherrypy mounts'''
    tackem_system = TackemSystemPlugin("library", "games", instance_name)
    cherrypy.tree.mount(
        Root("Game Library", key, tackem_system),
        CONFIG['webui']['baseurl'].value + key.replace(" ", "/") + "/",
        cfg()
    )


def cfg():
    '''generate the cherrypy conf'''
    return {}


class Root(HTMLTEMPLATE):
    '''ROOT OF PLUGINS WEBUI HERE'''
    @cherrypy.expose
    def index(self):
        '''index of plugin'''
        AUTHENTICATION.check_auth()
        index_page = self._name.replace("_", " ").title() + " ROOT"
        return self._template(index_page)
