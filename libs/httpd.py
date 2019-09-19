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
        self.__system = TackemSystemFull()

        cherrypy.config.update({
            'server.socket_host': '0.0.0.0',
            'server.socket_port': self.__system.config()['webui']['port'],
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
        baseurl = self.__system.get_baseurl()
        if self.__system.config()['firstrun']:
            cherrypy.tree.mount(first_run_root("", "", self.__system), baseurl,
                                conf_root)
        else:
            if not self.__system.config()['webui']['disabled']:
                cherrypy.tree.mount(main_root("", "", self.__system), baseurl, conf_root)
                if self.__system.get_auth().enabled():
                    cherrypy.tree.mount(Admin("Admin", "", self.__system),
                                        baseurl + "admin/", conf_root)
                for key in self.__system.systems():
                    #load system webpages into cherrypy
                    if self.__system.system(key).plugin_link().SETTINGS.get('single_instance', True):
                        self.__system.system(key).plugin_link().www.mounts(key)
                    else:
                        instance_name = key.split()[-1]
                        self.__system.system(key).plugin_link().www.mounts(key, instance_name)
            if self.__system.config()['api']['enabled']:
                cherrypy.tree.mount(API(), baseurl + "api/", conf_api)
            if self.__system.config()['scraper']['enabled']:
                scraper.mounts()

    def start(self):
        '''Start the server'''
        cherrypy.engine.start()

    def stop(self):
        '''Stop the server'''
        cherrypy.engine.exit()
        cherrypy.server.httpserver = None
