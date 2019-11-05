'''System for downloading plugins'''
import cherrypy
from libs.html_template import HTMLTEMPLATE
import libs.html_parts as html_parts
from system.plugin_downloader import TackemSystemPluginDownloader


class PluginDownloader(HTMLTEMPLATE):
    '''Plugin Downloader'''

    @cherrypy.expose
    def index(self) -> str:
        '''Index Page'''
        if not self._tackem_system.auth.is_admin():
            raise cherrypy.HTTPError(status=401)
        return self._template(
            plugin_download_page(True),
            False,
            javascript="plugin_downloader/javascript"
        )

    @cherrypy.expose
    def javascript(self) -> str:
        '''Javascript File'''
        if not self._tackem_system.auth.is_admin():
            raise cherrypy.HTTPError(status=401)
        return str(open("www/javascript/plugindownloader.js", "r").read())



def plugin_download_page(full_system: bool = True) -> str:
    '''returns the web page for choosing plugins'''
    TackemSystemPluginDownloader().get_github_plugins()
    TackemSystemPluginDownloader().get_local_plugins()
    html = "<h2>GITHUB PLUGINS</h2>"
    plugin_count = 0
    panels_html = ""
    for plugin in TackemSystemPluginDownloader().github_plugins:
        title = plugin['plugin_type'] + " - " + plugin['plugin_name']
        loaded = False
        if plugin['downloaded']:
            loaded = TackemSystemPluginDownloader().is_plugin_loaded(
                plugin['plugin_type'],
                plugin['plugin_name']
            )
            if loaded:
                plugin_count += 1

        clear_config = html_parts.input_button_with_data(
            "Clear Config",
            class_name="pluginbutton",
            data={'plugin':plugin['name']},
            outer_div=False,
            enabled=not loaded,
            visible=(full_system and plugin['downloaded'])
        )
        clear_database = html_parts.input_button_with_data(
            "Clear Database",
            class_name="pluginbutton",
            data={'plugin':plugin['name']},
            outer_div=False,
            enabled=not loaded,
            visible=(full_system and plugin['downloaded'])
        )
        add_remove = html_parts.input_button_with_data(
            ("Delete" if plugin['downloaded'] else "Download"),
            class_name="pluginbutton",
            data={'plugin':plugin['name']},
            outer_div=False
        )

        stop_start_action = ""
        stop_start_enabled = True
        stop_start_visible = False

        if full_system:
            stop_start_visible = plugin['downloaded']
            stop_start_action = "Stop" if loaded else "Start"
        else:
            stop_start_action = "Reload"
            stop_start_visible = plugin['downloaded'] and not loaded

        start_stop = html_parts.input_button_with_data(
            stop_start_action,
            class_name="pluginbutton",
            data={'plugin':plugin['name']},
            outer_div=False,
            enabled=stop_start_enabled,
            visible=stop_start_visible
        )
        readme = TackemSystemPluginDownloader().get_readme_as_html(
            plugin['plugin_type'],
            plugin['plugin_name']
        )
        if readme is None:
            readme = plugin['description']
        panels_html += html_parts.plugin_panel(title, readme, clear_config,
                                               clear_database, start_stop, add_remove)
    html += panels_html
    html += "<h2>LOCAL PLUGINS</h2>"
    panels_html = ""
    for plugin in TackemSystemPluginDownloader().local_plugins:
        if not plugin['offical']:
            title = plugin['plugin_type'] + " - " + plugin['plugin_name']
            offical = ""
            if plugin['repo']:
                offical = "[repo]"
            panels_html += "<H4>" + title + "</H4>" + offical
    html += panels_html
    html += html_parts.hidden("plugin_count", str(plugin_count), True)
    if full_system:
        return html
    html += html_parts.form("/", html_parts.hidden_page_index(3), "Next", "")
    if plugin_count == 0:
        html += '<script>$("button").prop("disabled", true);</script>'

    return html
