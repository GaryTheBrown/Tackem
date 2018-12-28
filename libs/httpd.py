'''HTTPD SYSTEM'''
import sys
import cherrypy
from www.first_run import Root as first_run_root
from www.root import Root as main_root
from libs.api import API

class Httpd():
    '''HTTPD CLASS'''
    def __init__(self, config, systems=False, plugins=False, first_run=False):
        self._config = config
        self._systems = systems
        self._plugins = plugins
        self._first_run = first_run

        cherrypy.config.update({
            'server.socket_host': '0.0.0.0',
            'server.socket_port': self._config['webui']['port'],
            'server.threadPool':10,
            'server.environment':"production",
            'log.screen': False,
            'log.access_file': '',
            'log.error_file': ''
        })
        conf_root = {
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': sys.path[0] + '/www/static/'
            }
        }
        conf_api = {
            '/':{
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/plain')]
            }
        }
        if first_run:
            cherrypy.tree.mount(first_run_root("Setup System",
                                               self._systems,
                                               self._plugins,
                                               self._config),
                                '/',
                                conf_root)
        else:
            baseurl = "/"
            if self._config['webui']['baseurl'] == "":
                self._config['webui']['baseurl'] = baseurl
            if self._config['webui']['baseurl'] != baseurl:
                baseurl = self._config['webui']['baseurl'] + "/"
            if self._config['webui']['enabled']:
                cherrypy.tree.mount(main_root("", self._systems, self._plugins, self._config),
                                    baseurl, conf_root)
                for key in self._systems:
                    #load system root
                    cherrypy.tree.mount(
                        self._systems[key].plugin_link().www.Root(key, self._systems,
                                                                  self._plugins,
                                                                  self._config),
                        baseurl + key.replace(" ", "/") + "/",
                        self._systems[key].plugin_link().www.cfg(self._config))

            if self._config['api']['enabled']:
                cherrypy.tree.mount(API(self._systems, self._plugins, self._config),
                                    baseurl + "api/", conf_api)

    def start(self):
        '''Start the server'''
        cherrypy.engine.start()

    def stop(self):
        '''Stop the server'''
        cherrypy.engine.exit()
        cherrypy.server.httpserver = None
