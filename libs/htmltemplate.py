'''HTML TEMPLATE'''
from libs.startup_arguments import PROGRAMNAME, PROGRAMVERSION

class HTMLTEMPLATE():
    '''Template Base Class For All WWW SYSTEMS'''

    _javascript_line = '<script src="%%LOCATION%%"></script>'

    def __init__(self, name, systems=None, plugins=None, config=None):
        self._name = name
        self._systems = systems
        self._plugins = plugins
        self._config = config

    def _template(self, body, navbar=True, replace=None, javascript=None):
        '''Create The Template Layout'''
        if not isinstance(replace, dict):
            replace = {}

        replace["PROGRAMNAMEFULL"] = PROGRAMNAME.upper()
        if self._name != "":
            replace["PROGRAMNAMEFULL"] += " - " + self._name.replace("_", " ").upper()

        replace["PROGRAMNAME"] = PROGRAMNAME.upper()
        replace["PROGRAMVERSION"] = PROGRAMVERSION
        if isinstance(navbar, str):
            replace["NAVBAR"] = navbar
        elif navbar:
            replace["NAVBAR"] = self._navbar()
        else:
            replace["NAVBAR"] = ""

        replace["JAVASCRIPTEXTRA"] = ""
        if isinstance(javascript, list):
            for key in javascript:
                replace["JAVASCRIPTEXTRA"] += self._javascript_line.replace("%%LOCATION%%", key)
        elif isinstance(javascript, str):
            replace["JAVASCRIPTEXTRA"] = self._javascript_line.replace("%%LOCATION%%", javascript)

        template_page = self._header()
        template_page += body
        template_page += self._footer()
        for key in replace:
            template_page = template_page.replace("%%" + key.upper() + "%%", replace[key])
        return template_page

    def _header(self):
        '''Header Of Pages'''
        return self.get_page_file("www/html/head.html")

    def _navbar(self):
        '''Navigation Bar For System'''
        nav_page = self.get_page_file("www/html/navbar.html")
        nav = ''
        if not self._systems is None:
            nav_list = {}

            for key in self._systems:
                system_type = self._plugins[self._systems[key].plugin_link()].SETTINGS['type']
                if not system_type in nav_list:
                    nav_list[system_type] = []
                nav_list[system_type].append(key)
            nav = ''
            for key in sorted(nav_list):
                if key in self._systems:
                    item = ''
                    item_class = []

                    item_class.append('nav-item')

                    if key == self._name:
                        item_class.append('active')
                    item += '<li class="' + " ".join(item_class) + '">'
                    if key != self._name:
                        item += '<a href="'
                        item += self._config.get("webui", {}).get("baseurl", "") + '/'+ key + '/">'
                    else:
                        item += '<a>'
                    item += key.title().replace("_", "&nbsp;")
                    item += '</a>'
                    item += '</li>'
                    nav += item
                else:
                    nav += self._dropdown_nav(key.title(), nav_list[key])

        return nav_page.replace("%%NAVBARITEMS%%", nav)

    def _footer(self):
        '''Footer OF THE PAGE'''
        return self.get_page_file("www/html/footer.html")

    def _dropdown_nav(self, name, items):
        data = '<li class="nav-item dropdown">'
        data += '<a class="nav-link dropdown-toggle" id="%%PLUGINNAME%%_' + name
        data += '" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" href="#">'
        data += name

        data += '</a>'
        data += '<div class="dropdown-menu" aria-labelledby="dropdown_'+ name +'">'
        for key in items:
            item_class = []
            item_class.append('dropdown-item')
            if key == self._name:
                item_class.append('active')
            item = '<a '
            item += 'class="' + " ".join(item_class) + '"'
            if key != self._name:
                baseurl = self._config.get("webui", {}).get("baseurl", "")
                item += 'href="' + baseurl + '/'+ key + '/"'
            item += ">"
            item += key.title().replace("_", "&nbsp;")
            item += '</a>'
            data += item
        data += '</div>'
        data += '</li>'

        return data

    def get_page_file(self, file_to_grab):
        '''Grabs the page and does the global replaces'''
        baseurl = self._config.get("webui", {}).get("baseurl", "")
        page = str(open(file_to_grab, 'r').read())
        page = page.replace("%%BASEURL%%", baseurl)
        return page
