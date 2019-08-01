'''HTTPD SYSTEM'''
import os
import cherrypy
from www.first_run import Root as first_run_root
from www.root import Root as main_root
from www.admin import Admin
from libs.api import API
from libs import scraper
from system.full import TackemSystemFull

class Httpd():
    '''HTTPD CLASS'''
    def __init__(self):
        self._system = TackemSystemFull()

        cherrypy.config.update({
            'server.socket_host': '0.0.0.0',
            'server.socket_port': self._system.config()['webui']['port'],
            'server.threadPool':10,
            'server.environment':"production",
            'log.screen': False,
            'log.access_file': '',
            'log.error_file': '',
        })
        conf_root = {
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.getcwd() + '/www/static/'
            }
        }
        conf_api = {
            '/':{
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/plain')]
            }
        }
        baseurl = self._system.get_baseurl()
        if self._system.config()['firstrun']:
            cherrypy.tree.mount(first_run_root("", "", self._system), baseurl,
                                conf_root)
        else:
            if not self._system.config()['webui']['disabled']:
                cherrypy.tree.mount(main_root("", "", self._system), baseurl, conf_root)
                if self._system.get_auth().enabled():
                    cherrypy.tree.mount(Admin("Admin", "", self._system),
                                        baseurl + "admin/", conf_root)
                for key in self._system.systems():
                    #load system webpages into cherrypy
                    if self._system.system(key).plugin_link().SETTINGS.get('single_instance', True):
                        self._system.system(key).plugin_link().www.mounts(key)
                    else:
                        instance_name = key.split()[-1]
                        self._system.system(key).plugin_link().www.mounts(key, instance_name)
            if self._system.config()['api']['enabled']:
                cherrypy.tree.mount(API(), baseurl + "api/", conf_api)
            if self._system.config()['scraper']['enabled']:
                scraper.mounts()

    def start(self):
        '''Start the server'''
        cherrypy.engine.start()

    def stop(self):
        '''Stop the server'''
        cherrypy.engine.exit()
        cherrypy.server.httpserver = None
