'''Script For the first Run Of The System'''
import cherrypy
from libs.htmltemplate import HTMLTEMPLATE
from libs.config import post_config_settings, plugin_config_page
from libs.config import root_config_page, get_multi_setup
from libs.config import javascript as config_javascript
from libs.root_event import RootEvent

class Root(HTMLTEMPLATE):
    '''Setup Script'''
    @cherrypy.expose
    def index(self, **kwargs):
        '''Index Page'''
        if cherrypy.request.method == "POST" and kwargs:
            if "page_index" in kwargs:
                return self._post_action(kwargs)

        page = str(open("www/first_run/index.html", "r").read())
        return self._template(page, False)

    @cherrypy.expose
    def javascript(self):
        '''Javascript File'''
        return config_javascript()

    @cherrypy.expose
    def get_multi_setup(self, plugin, name=""):
        '''Return the information needed for the setup of the plugin'''
        return get_multi_setup(self._plugins, plugin, {}, name)

    def _post_action(self, kwargs):
        '''the part of the script to do all of the pages & updates of the config'''
        post_config_settings(kwargs, self._config, self._plugins)
        javascript = "/javascript"

        if kwargs["page_index"] == "1":
            return self._template(root_config_page(), False, javascript=javascript)

        elif kwargs["page_index"] == "2":
            return self._template(plugin_config_page(self._plugins),
                                  False, javascript=javascript)

        elif kwargs["page_index"] == "3":
            try:
                self._config.write()
            except OSError:
                print("ERROR WRITING CONFIG FILE")
            RootEvent().reboot()
            html = """RESTARTING NOW... refreshing in 10 seconds...
<script>
    window.setTimeout(function() {
        window.location.href = '/welcome';
        return false;
    }, 10000);
</script>"""

            return self._template(html, False)
