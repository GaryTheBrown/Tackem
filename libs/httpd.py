'''HTTPD SYSTEM'''
import os
import cherrypy
# from www.first_run import Root as first_run_root
from www.root import Root
from www.admin import Admin
# from www.plugin_downloader import PluginDownloader
from api import API
from libs import scraper
from libs.error_pages import setup_error_pages
from libs.startup_arguments import THEMEFOLDERLOCATION
from config_data import CONFIG
from system.full import TackemSystemFull


class Httpd():
    '''HTTPD CLASS'''

    def __init__(self):
        self.__system = TackemSystemFull()

        cherrypy.config.update({
            'server.socket_host': '0.0.0.0',
            'server.socket_port': CONFIG['webui']['port'].value,
            'server.threadPool': 10,
            'server.environment': "production",
            'log.screen': False,
            'log.access_file': '',
            'log.error_file': '',
        })

        setup_error_pages(e500=False)

        conf_root = {
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.getcwd() + '/www/static/'
            }
        }
        for theme in next(os.walk(THEMEFOLDERLOCATION))[1]:
            conf_root['/themes/' + theme] = {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.getcwd() + '/' + THEMEFOLDERLOCATION + theme + "/static"
            }

        conf_api = {
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/plain')],
                'tools.json_out.on': True
            }
        }

        baseurl = CONFIG['webui']['baseurl'].value

        cherrypy.tree.mount(Root("", "", self.__system), baseurl, conf_root)
        cherrypy.tree.mount(Admin("Admin", "", self.__system),
                            baseurl + "admin/", conf_root)
        for key in self.__system.systems:
            # load system webpages into cherrypy
            plugin_link = self.__system.system(key).plugin_link()
            if plugin_link.SETTINGS.get('single_instance', True):
                plugin_link.www.mounts(key)
            else:
                instance_name = key.split()[-1]
                plugin_link.www.mounts(key, instance_name)

        # scraper.mounts()
        cherrypy.tree.mount(API(), baseurl + "api/", conf_api)

    def start(self) -> None:
        '''Start the server'''
        cherrypy.engine.start()

    def stop(self) -> None:
        '''Stop the server'''
        cherrypy.engine.exit()
        cherrypy.server.httpserver = None
