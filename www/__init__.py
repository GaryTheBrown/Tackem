"""Webserver"""
import os

import cherrypy

from api import API
from data.config import CONFIG
from data.database.system import UPLOAD_DB
from libs.database import Database
from libs.database.messages.table import SQLTable
from libs.file import File
from www.template import Template

cherrypy.tools.template = Template()  # noqa: E402
from www.controller import Root  # noqa: E402


class Webserver:
    """Webserver"""

    __running = False

    @classmethod
    def start(cls):
        """starts the webserver"""
        if cls.__running:
            return

        Database.call(SQLTable(UPLOAD_DB))

        def error_page(status, message, traceback, version) -> str:
            """error page"""
            return f"Error {status}"

        cherrypy.config.update(
            {
                "error_page.400": error_page,
                "error_page.401": error_page,
                "error_page.403": error_page,
                "error_page.404": error_page,
                "error_page.405": error_page,
                # "error_page.500": error_page,
                "server.socket_host": CONFIG["webui"]["socket"].value,
                "server.socket_port": CONFIG["webui"]["port"].value,
                "server.threadPool": 10,
                "server.environment": "production",
                "server.max_request_body_size": 0,
                "server.socket_timeout": 60,
                "log.screen": False,
                "log.access_file": "",
                "log.error_file": "",
            }
        )

        conf_www = {
            "/img": {
                "tools.staticdir.on": True,
                "tools.staticdir.dir": os.getcwd() + "/www/static/img/",
            },
            "/js": {
                "tools.staticdir.on": True,
                "tools.staticdir.dir": os.getcwd() + "/www/static/js/",
            },
            "/style.css": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": os.getcwd() + "/www/static/style.css",
            },
            "/upload": {"response.timeout": 3600},
        }

        conf_api = {
            "/": {
                "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
                "tools.response_headers.on": True,
                "tools.response_headers.headers": [("Content-Type", "text/plain")],
                "tools.json_out.on": True,
            }
        }

        baseurl = CONFIG["webui"]["baseurl"].value

        cherrypy.tree.mount(Root(), baseurl, conf_www)
        cherrypy.tree.mount(API(), baseurl + "api/", conf_api)

        File.mkdir(File.location(CONFIG["webui"]["uploadlocation"].value))

        cherrypy.engine.start()
        cls.__running = True

    @classmethod
    def stop(cls):
        """stops the Webserver"""
        if cls.__running:
            cherrypy.engine.exit()
            cherrypy.server.httpserver = None
            cls.__running = False
