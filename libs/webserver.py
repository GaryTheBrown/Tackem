'''Webserver'''
from www.upload import Upload
from cherrypy.process.wspbus import bus
from www.ripper import RipperRoot
from www.ripper.drive import RipperDrive
from libs.ripper import Ripper
from libs.file import File
import os
import cherrypy
from www.root import Root
from www.admin import Admin
from api import API
from libs.error_pages import setup_error_pages
from data import THEMEFOLDERLOCATION
from data.config import CONFIG
from data.config import CONFIG
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE
from libs.database import Database
from libs.database.messages import SQLTable
from data.database.system import UPLOAD_DB
class Webserver:
    '''Webserver'''
    __running = False

    @classmethod
    def start(cls):
        '''starts the webserver'''
        if cls.__running:
            return

        Database.call(SQLTable(UPLOAD_DB))

        HTMLTEMPLATE.set_baseurl(CONFIG['webui']['baseurl'].value)

        cherrypy.config.update({
            'server.socket_host': '0.0.0.0',
            'server.socket_port': CONFIG['webui']['port'].value,
            'server.threadPool': 10,
            'server.environment': "production",
            'server.max_request_body_size' : 0,
            'server.socket_timeout' : 60,
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

        ripper_cfg = CONFIG['ripper']
        conf_ripper = {
            '/tempvideo': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': File.location(ripper_cfg['locations']['videoripping'].value)
            },
            '/tempaudio': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': File.location(ripper_cfg['locations']['audioripping'].value)
            }
        }

        conf_upload = {
            "/":{
                'response.timeout': 3600
            }
        }

        baseurl = CONFIG['webui']['baseurl'].value

        cherrypy.tree.mount(Root("", ""), baseurl, conf_root)
        cherrypy.tree.mount(Admin("Admin", ""), baseurl + "admin/", conf_root)
        cherrypy.tree.mount(API(), baseurl + "api/", conf_api)
        cherrypy.tree.mount(Upload("Upload", ""), baseurl + "upload/", conf_upload)

        File.mkdir(File.location(CONFIG['webui']['uploadlocation'].value))

        if Ripper.running:
            ripper = RipperRoot("Ripper", "")
            ripper.drives = RipperDrive("Ripper Drives", "")
            # ripper.videolabeler = VideoLabeler("Ripper Video Labeler", "")
            # ripper.converter = Converter("Ripper Video Converter", "")
            cherrypy.tree.mount(ripper, baseurl + "ripper/", conf_ripper)

        HTMLSystem.set_theme(CONFIG['webui']['theme'].value)
        cherrypy.engine.start()
        cls.__running = True

    @classmethod
    def stop(cls):
        '''stops the Webserver'''
        if cls.__running:
            cherrypy.engine.exit()
            cherrypy.server.httpserver = None
            cls.__running = False
