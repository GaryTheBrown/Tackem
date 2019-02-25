'''HTML TEMPLATE'''
import libs.html_parts as html_part

class HTMLTEMPLATE():
    '''Template Base Class For All WWW SYSTEMS'''
    def __init__(self, name, key, systems, plugins, config, auth,
                 base_stylesheet=None, base_javascript=None):
        self._key = key
        self._systems = systems
        self._plugins = plugins
        self._global_config = config
        self._auth = auth
        self._name = name
        self._base_stylesheet = base_stylesheet
        self._base_javascript = base_javascript
        self._baseurl = self._global_config.get("webui", {}).get("baseurl", "/")

        if key != "":
            self._system = systems[key]
            split_key = key.split(" ")
            self._plugin = plugins[split_key[0]][split_key[1]]
            if len(split_key) == 2:
                self._config = config['plugins'][split_key[0]][split_key[1]]
            elif len(split_key) == 3:
                self._config = config['plugins'][split_key[0]][split_key[1]][split_key[2]]

    def _template(self, body, navbar=True, javascript=None, stylesheet=None):
        '''Create The Template Layout'''
        navbar_html = ""
        if isinstance(navbar, str):
            navbar_html = navbar
        elif navbar:
            navbar_html = self._navbar()
        javascript_extra_html = ""
        if isinstance(self._base_javascript, list):
            for key in self._base_javascript:
                javascript_extra_html += html_part.script_link(key)
        elif isinstance(self._base_javascript, str):
            javascript_extra_html = html_part.script_link(self._base_javascript)
        if isinstance(javascript, list):
            for key in javascript:
                javascript_extra_html += html_part.script_link(key)
        elif isinstance(javascript, str):
            javascript_extra_html = html_part.script_link(javascript)
        stylesheet_extra_html = ""
        if isinstance(self._base_stylesheet, list):
            for key in self._base_stylesheet:
                stylesheet_extra_html += html_part.stylesheet_link(key)
        elif isinstance(self._base_stylesheet, str):
            stylesheet_extra_html = html_part.stylesheet_link(self._base_stylesheet)
        if isinstance(stylesheet, list):
            for key in stylesheet:
                stylesheet_extra_html += html_part.stylesheet_link(key)
        elif isinstance(stylesheet, str):
            stylesheet_extra_html = html_part.stylesheet_link(stylesheet)
        baseurl = self._global_config.get("webui", {}).get("baseurl", "")
        title = ""
        if self._key is not "":
            if self._name != "":
                title = " - " + self._name.title()
            else:
                title = " - " + self._key.replace(" ", " - ").title()
        return html_part.master_template(title, body, javascript_extra_html, stylesheet_extra_html,
                                         baseurl, navbar_html)

    def _error_page(self, code):
        '''Shows the error Page'''
        #if not any codes bellow or 404
        page = '<h1 class="text-center">404 Not Found</h1>'
        if code == 401:
            page = '<h1 class="text-center">401 Not Authorised</h1>'
        return self._template(page, False)

    def _navbar(self):
        '''Navigation Bar For System'''
        nav_items_html = ""
        if not self._auth.enabled():
            nav_items_html = self._navbar_item()
        elif self._auth.check_logged_in():
            nav_items_html = self._navbar_item()

        navbar_right_html = ""
        if self._auth.is_admin() or not self._auth.enabled():
            navbar_admin = ""
            navbar_admin += html_part.navbar_item("Config", "config")
            if self._auth.enabled() and self._auth.is_admin():
                navbar_admin += html_part.navbar_item("Users", "admin/users")
            navbar_admin += html_part.navbar_item("Reboot", "reboot")
            navbar_admin += html_part.navbar_item("Shutdown", "shutdown")
            navbar_right_html += html_part.navbar_dropdown_right("Admin", "admin", navbar_admin)
        if self._auth.enabled():
            if self._auth.check_logged_in():
                navbar_user = ""
                navbar_user += html_part.navbar_item("Logout", "logout")
                navbar_user += html_part.navbar_item("Change Password", "password")
                navbar_right_html += html_part.navbar_dropdown_right("User", "user", navbar_user)
            else:
                navbar_right_html += html_part.navbar_item("Login", "login")
        return html_part.navbar_master(nav_items_html, navbar_right_html)

    def _navbar_item(self):
        '''Navigation Bar For System'''
        nav_items_html = ""
        nav_list = {}
        for key in self._systems:
            key_list = key.split(" ")
            if not key_list[0] in nav_list:
                if len(key_list) is 1:
                    nav_list[key_list[0]] = key
                    continue
                nav_list[key_list[0]] = {}
            if not key_list[1] in nav_list[key_list[0]]:
                if len(key_list) is 2:
                    nav_list[key_list[0]][key_list[1]] = key
                    continue
                nav_list[key_list[0]][key_list[1]] = {}
            if not key_list[2] in nav_list[key_list[0]][key_list[1]]:
                nav_list[key_list[0]][key_list[1]][key_list[2]] = key

        for key in sorted(nav_list):
            if isinstance(nav_list[key], str):
                if nav_list[key] is self._key:
                    nav_items_html += html_part.navbar_item_active(key)
                else:
                    nav_items_html += html_part.navbar_item(key, nav_list[key])
            else:
                layer2 = ""
                for key2 in sorted(nav_list[key]):
                    if isinstance(nav_list[key][key2], str):
                        if nav_list[key][key2] is self._key:
                            layer2 += html_part.navbar_item_active(key2)
                        else:
                            layer2 += html_part.navbar_item(key2, nav_list[key][key2])
                    else:
                        layer3 = ""
                        for key3 in sorted(nav_list[key][key2]):
                            if nav_list[key][key2][key3] is self._key:
                                layer3 += html_part.navbar_item_active(key3)
                            else:
                                layer3 += html_part.navbar_item(key3, nav_list[key][key2][key3])
                        layer2 += html_part.navbar_drop_right(key2, key + key2, layer3)
                nav_items_html += html_part.navbar_dropdown(key, key, layer2)
        return nav_items_html
