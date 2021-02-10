'''Webserver'''
import os
import cherrypy
from www.root import Root
from www.admin import Admin
from api import API
from libs.error_pages import setup_error_pages
from data import THEMEFOLDERLOCATION
from data.config import CONFIG
from typing import Optional
from data.config import CONFIG
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE
class Webserver:
    '''Webserver'''
    __running = False

    @classmethod
    def start(cls):
        '''starts the webserver'''
        if cls.__running:
            return

        HTMLTEMPLATE.set_baseurl(CONFIG['webui']['baseurl'].value)

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

        cherrypy.tree.mount(Root("", ""), baseurl, conf_root)
        cherrypy.tree.mount(Admin("Admin", ""), baseurl + "admin/", conf_root)
        cherrypy.tree.mount(API(), baseurl + "api/", conf_api)

        HTMLSystem.set_theme(CONFIG['webui']['theme'].value)
        cherrypy.engine.start()

    @classmethod
    def stop(cls):
        '''stops the Webserver'''
        if cls.__running:
            cherrypy.engine.exit()
            cherrypy.server.httpserver = None
