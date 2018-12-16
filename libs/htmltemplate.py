'''HTML TEMPLATE'''
import libs.html_parts as html_part

class HTMLTEMPLATE():
    '''Template Base Class For All WWW SYSTEMS'''

    def __init__(self, name, systems=None, plugins=None, config=None):
        self._name = name
        self._systems = systems
        self._plugins = plugins
        self._config = config

    def _template(self, body, navbar=True, javascript=None):
        '''Create The Template Layout'''
        navbar_html = ""
        if isinstance(navbar, str):
            navbar_html = navbar
        elif navbar:
            navbar_html = self._navbar()
        javascript_extra_html = ""
        if isinstance(javascript, list):
            for key in javascript:
                javascript_extra_html += html_part.script_link(key)
        elif isinstance(javascript, str):
            javascript_extra_html = html_part.script_link(javascript)
        baseurl = self._config.get("webui", {}).get("baseurl", "")
        title = ""
        if self._name is not "":
            title = " - " + self._name.replace(" ", " - ").capitalize()
        return html_part.master_template(title, body, javascript_extra_html, baseurl, navbar_html)

    def _navbar(self):
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
                if nav_list[key] is self._name:
                    nav_items_html += html_part.navbar_item_active(key)
                else:
                    nav_items_html += html_part.navbar_item(key, nav_list[key])
            else:
                layer2 = ""
                for key2 in sorted(nav_list[key]):
                    if isinstance(nav_list[key][key2], str):
                        if nav_list[key][key2] is self._name:
                            layer2 += html_part.navbar_item_active(key2)
                        else:
                            layer2 += html_part.navbar_item(key2, nav_list[key][key2])
                    else:
                        layer3 = ""
                        for key3 in sorted(nav_list[key][key2]):
                            if nav_list[key][key2][key3] is self._name:
                                layer3 += html_part.navbar_item_active(key3)
                            else:
                                layer3 += html_part.navbar_item(key3, nav_list[key][key2][key3])
                        layer2 += html_part.navbar_dropdown_right(key2, key + key2, layer3)
                nav_items_html += html_part.navbar_dropdown(key, key, layer2)
        return html_part.navbar_master(nav_items_html)
