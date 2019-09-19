'''HTML TEMPLATE'''
import libs.html_parts as html_part

class HTMLTEMPLATE():
    '''Template Base Class For All WWW SYSTEMS'''
    def __init__(self, name, key, tackem_system, base_stylesheet=None, base_javascript=None):
        self._tackem_system = tackem_system
        self._name = name
        self._key = key
        self._base_stylesheet = base_stylesheet
        self._base_javascript = base_javascript

        if key != "":
            self._plugin = self._tackem_system.plugin()
            self._config = self._tackem_system.config()

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
        baseurl = self._tackem_system.get_baseurl()
        title = ""
        if self._key != "":
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
        return html_part.navbar_master(self._navbar_left_items(), self._navbar_right_items())

    def _navbar_left_items(self):
        '''Navigation Bar Left Items For The System'''
        nav_items_html = ""
        if self._tackem_system.get_auth().enabled():
            if not self._tackem_system.get_auth().check_logged_in():
                return nav_items_html
        nav_list = {}
        for key in self._tackem_system.system_keys():
            key_list = key.split(" ")
            if not key_list[0] in nav_list:
                if len(key_list) != 1:
                    nav_list[key_list[0]] = key
                    continue
                nav_list[key_list[0]] = {}
            if not key_list[1] in nav_list[key_list[0]]:
                if len(key_list) != 2:
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

    def _navbar_right_items(self):
        '''Navigation Bar Left Items For The System'''
        navbar_about_html = html_part.navbar_item("About", "about")
        navbar_config_html = html_part.navbar_item("Config", "config")
        navbar_plugin_download_html = html_part.navbar_item("Plugin Download", "plugin_download")
        navbar_users_html = html_part.navbar_item("Users", "admin/users")
        navbar_login_html = html_part.navbar_item("Login", "login")
        navbar_logout_html = html_part.navbar_item("Logout", "logout")
        navbar_password_html = html_part.navbar_item("Change Password", "password")
        navbar_reboot_html = html_part.navbar_item("Reboot", "reboot")
        navbar_shutdown_html = html_part.navbar_item("Shutdown", "shutdown")

        navbar_right_html = navbar_about_html
        if self._tackem_system.get_auth().enabled():
            if self._tackem_system.get_auth().check_logged_in():
                if self._tackem_system.get_auth().is_admin():
                    admin_html = navbar_config_html
                    admin_html += navbar_plugin_download_html
                    admin_html += navbar_users_html
                    admin_html += navbar_reboot_html
                    admin_html += navbar_shutdown_html
                    navbar_right_html += html_part.navbar_dropdown_right("Admin", "admin",
                                                                         admin_html)
                user_html = navbar_password_html
                user_html += navbar_logout_html
                navbar_right_html += html_part.navbar_dropdown_right("User", "user", user_html)
            else:
                navbar_right_html += navbar_login_html
        else:
            system_html = navbar_config_html
            system_html += navbar_reboot_html
            system_html += navbar_shutdown_html
            navbar_right_html += html_part.navbar_dropdown_right("System", "system", system_html)
        return navbar_right_html
