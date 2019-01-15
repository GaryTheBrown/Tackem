'''WEBUI FOR PLUGIN'''
import cherrypy
from libs.html_template import HTMLTEMPLATE

LAYOUT = {}
def mounts(plugin_base_url, key, systems, plugins, config):
    '''where the system creates the cherrypy mounts'''
    cherrypy.tree.mount(Root(key, systems, plugins, config),
                        plugin_base_url,
                        cfg(config))

def cfg(config):
    '''generate the cherrypy conf'''
    return {}

class Root(HTMLTEMPLATE):
    '''ROOT OF PLUGINS WEBUI HERE'''
    @cherrypy.expose
    def index(self):
        '''index of plugin'''
        index_page = self._name.replace("_", " ").title() + " ROOT"
        return self._template(index_page)
