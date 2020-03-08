'''Script For the Admin System'''
import cherrypy
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE
from libs.authenticator import AUTHENTICATION
from libs.config.html.post_to_config import post_config_settings
from config_data import CONFIG
from system.plugin_downloader import TackemSystemPluginDownloader

class Admin(HTMLTEMPLATE):
    '''Admin'''


    @cherrypy.expose
    def config(self, **kwargs) -> str:
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
            title = plugin['plugin_type'] + " - " + plugin['plugin_name']
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
                PLUGINTYPE=plugin['plugin_type'],
                PLUGINNAME=plugin['plugin_name'],
                DESCRIPTION=readme,
                CLEARCONFIGDISABLED="" if plugin['downloaded'] and not is_loaded else "disabled",
                CLEARDATABASEDISABLED="" if plugin['downloaded'] and not is_loaded else "disabled",
                START="" if plugin['downloaded'] and not is_loaded else "disabled",
                STOP="" if is_loaded else "disabled",
                DOWNLOAD="disabled" if plugin['downloaded'] else "",
                REMOVE="" if plugin['downloaded'] else "disabled",
            )

        for plugin in TackemSystemPluginDownloader().local_plugins:
            if not plugin['offical']:
                title = plugin['plugin_type'] + " - " + plugin['plugin_name']
                offical = ""
                if plugin['repo']:
                    offical = "[repo]"
                local_plugin_html += "<H4>" + title + "</H4>" + offical

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
            users_html += HTMLSystem.part(
                "section/user",
                USERID=item['id'],
                NAME=item['username'],
                ISADMIN="checked" if item['is_admin'] else ""
            )
        return self._template(
            HTMLSystem.part(
                "pages/users",
                USERSHTML=users_html
            )
        )
