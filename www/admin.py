'''Script For the Admin System'''
import cherrypy
from typing import Any
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE
from libs.authenticator import AUTHENTICATION
from libs.config.html.post_to_config import post_config_settings
from data.config import CONFIG
from system.plugin_downloader import TackemSystemPluginDownloader

class Admin(HTMLTEMPLATE):
    '''Admin'''

    @cherrypy.expose
    def config(self, **kwargs: Any) -> str:
        '''Config System'''
        AUTHENTICATION.check_auth()
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPError(status=401)
        if kwargs:
            post_config_settings(kwargs)
            try:
                CONFIG.save()
            except OSError:
                print("ERROR WRITING CONFIG FILE")
        return self._template(CONFIG.html(), javascript="static/js/config.js")

    @cherrypy.expose
    def plugin_downloader(self) -> str:
        '''THe system for the plugin Downloader'''
        AUTHENTICATION.check_auth()
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPError(status=401)

        TackemSystemPluginDownloader().get_github_plugins()
        TackemSystemPluginDownloader().get_local_plugins()

        github_plugin_html = ""
        local_plugin_html = ""

        for plugin in TackemSystemPluginDownloader().github_plugins:
            title = f"{plugin['plugin_type']} - {plugin['plugin_name']}"
            readme = TackemSystemPluginDownloader().get_readme_as_html(
                plugin['plugin_type'],
                plugin['plugin_name']
            )
            if readme is None:
                readme = plugin['description']

            is_loaded = TackemSystemPluginDownloader().is_plugin_loaded(
                plugin['plugin_type'],
                plugin['plugin_name']
            )

            github_plugin_html += HTMLSystem.part(
                "section/plugindownloader",
                TITLE=title,
                PLUGINTYPE=plugin['plugin_type'].lower(),
                PLUGINNAME=plugin['plugin_name'].lower(),
                DESCRIPTION=readme,
                LOAD="" if plugin['downloaded'] and not is_loaded else "disabled",
                UNLOAD="" if is_loaded else "disabled",
                DOWNLOAD="disabled" if plugin['downloaded'] else "",
                UPDATE="" if plugin['downloaded'] and is_loaded else "disabled",
            )

        for plugin in TackemSystemPluginDownloader().local_plugins:
            if not plugin['offical']:
                title = f"{plugin['plugin_type']} - {plugin['plugin_name']}"
                offical = ""
                if plugin['repo']:
                    offical = "[repo]"
                local_plugin_html += f"<H4>{title}</H4>{offical}"

        page = HTMLSystem.part(
            "pages/plugindownloader",
            GITHUBPLUGINS=github_plugin_html,
            LOCALPLUGINS=local_plugin_html,
        )

        return self._template(page, javascript="static/js/plugindownloader.js")

    @cherrypy.expose
    def users(self) -> str:
        '''Grab the users info'''
        AUTHENTICATION.check_auth()
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPError(status=401)
        data = AUTHENTICATION.get_users()
        users_html = ""
        for item in data:
            admin = "checked" if item['is_admin'] else ""
            admin += " disabled" if item['id'] == 1 else ""
            users_html += HTMLSystem.part(
                "section/user",
                USERID=item['id'],
                NAME=item['username'],
                ISADMIN=admin
            )
        return self._template(
            HTMLSystem.part(
                "pages/users",
                USERSHTML=users_html
            ),
            javascript="static/js/users.js"
        )

    @cherrypy.expose
    def shutdown(self) -> str:
        '''shutdown the system page'''
        AUTHENTICATION.check_auth()
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPError(status=401)
        return self._template(
            HTMLSystem.part(
                "pages/shutdown"
            )
        )

    @cherrypy.expose
    def reboot(self) -> str:
        '''reboot the system page'''
        AUTHENTICATION.check_auth()
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPError(status=401)
        return self._template(
            HTMLSystem.part(
                "pages/reboot"
            )
        )
