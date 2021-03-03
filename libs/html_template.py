'''HTML TEMPLATE'''
from typing import List, Optional, Union
from data import PROGRAMVERSION
from data.config import CONFIG
from libs.authenticator import Authentication
from libs.html_system import HTMLSystem
from libs.ripper import Ripper

class HTMLTEMPLATE():
    '''Template Base Class For All WWW SYSTEMS'''
    _baseurl = "/"

    @classmethod
    def set_baseurl(cls, baseurl: str):
        '''sets the base url for use rather than accessing through the config each time'''
        cls._baseurl = baseurl

    def __init__(
            self,
            name: str,
            key: str,
            base_stylesheet: Optional[str] = None,
            base_javascript: Optional[str] = None
    ):
        self._name = name
        self._key = key
        self._base_stylesheet = base_stylesheet
        self._base_javascript = base_javascript

    def _template(
            self,
            body: str,
            navbar: bool = True,
            javascript: Optional[Union[List[str], str]] = None,
            stylesheet: Optional[Union[List[str], str]] = None
    ) -> str:
        '''Create The Template Layout'''
        navbar_html = ""
        if isinstance(navbar, str):
            navbar_html = navbar
        elif navbar:
            navbar_html = HTMLSystem.part(
                "navbar/master",
                NAVBARRIGHT=self._navbar_right_items(),
                NAVBARITEMS=self._navbar_left_items()
            )

        javascript_extra_html = ""
        if isinstance(self._base_javascript, list):
            for key in self._base_javascript:
                javascript_extra_html += HTMLSystem.script_link(key)
        elif isinstance(self._base_javascript, str):
            javascript_extra_html = HTMLSystem.script_link(
                self._base_javascript)

        if isinstance(javascript, list):
            for key in javascript:
                javascript_extra_html += HTMLSystem.script_link(key)
        elif isinstance(javascript, str):
            javascript_extra_html = HTMLSystem.script_link(javascript)

        stylesheet_extra_html = ""
        if isinstance(self._base_stylesheet, list):
            for key in self._base_stylesheet:
                stylesheet_extra_html += HTMLSystem.stylesheet_link(key)
        elif isinstance(self._base_stylesheet, str):
            stylesheet_extra_html = HTMLSystem.stylesheet_link(
                self._base_stylesheet)

        if isinstance(stylesheet, list):
            for key in stylesheet:
                stylesheet_extra_html += HTMLSystem.stylesheet_link(key)
        elif isinstance(stylesheet, str):
            stylesheet_extra_html = HTMLSystem.stylesheet_link(stylesheet)

        title = ""
        if self._key != "":
            if self._name != "":
                title = f" - {self._name.title()}"
            else:
                temp_key = self._key.replace(" ", " - ").title()
                title = f" - {temp_key}"

        return HTMLSystem.part(
            "template",
            JAVASCRIPTEXTRA=javascript_extra_html,
            STYLESHEETEXTRA=stylesheet_extra_html,
            NAVBAR=navbar_html,
            BODY=body,
            BASEURL=self._baseurl,
            PROGRAMVERSION=PROGRAMVERSION,
            TITLE=title
        )

    def _error_page(self, code: int) -> str:
        '''Shows the error Page'''
        # if not any codes bellow or 404
        page = '<h1 class="text-center">404 Not Found</h1>'
        if code == 401:
            page = '<h1 class="text-center">401 Not Authorised</h1>'
        return self._template(page, False)

    def _navbar_left_items(self) -> str:
        '''Navigation Bar Left Items For The System'''
        nav_items_html = ""
        if not Authentication.check_logged_in():
            return nav_items_html

        ripper_html = navbar_item("Ripper", "ripper")

        if Ripper.running:
            nav_items_html += ripper_html
        return nav_items_html

    def _navbar_right_items(self) -> str:
        '''Navigation Bar Left Items For The System'''
        navbar_about_html = navbar_item("About", "about")
        navbar_item_html = navbar_item("CONFIG", "admin/config")
        navbar_users_html = navbar_item("Users", "admin/users")
        navbar_login_html = navbar_item("Login", "login")
        navbar_logout_html = navbar_item("Logout", "logout")
        navbar_password_html = navbar_item("Change Password", "password")
        navbar_reboot_html = navbar_item("Reboot", "admin/reboot")
        navbar_shutdown_html = navbar_item("Shutdown", "admin/shutdown")

        navbar_right_html = navbar_about_html
        if Authentication.check_logged_in():
            if Authentication.is_admin():
                admin_html = navbar_item_html
                admin_html += navbar_users_html
                admin_html += navbar_reboot_html
                admin_html += navbar_shutdown_html
                navbar_right_html += navbar_dropdown_right(
                    "Admin", "admin", admin_html)
            user_html = navbar_password_html
            user_html += navbar_logout_html
            navbar_right_html += navbar_dropdown_right(
                "User", "user", user_html)
        else:
            navbar_right_html += navbar_login_html
        return navbar_right_html

def navbar_dropdown(title: str, dropdown_id: str, items: str) -> str:
    '''A Navbar Item (not active)'''
    return HTMLSystem.part(
        "navbar/dropdown",
        TITLE=title.title(),
        DROPDOWNID=dropdown_id,
        ITEMS=items
    )

def navbar_dropdown_right(title: str, dropdown_id: str, items: str) -> str:
    '''A Navbar Item right aligned (not active)'''
    return HTMLSystem.part(
        "navbar/dropdownright",
        TITLE=title.title(),
        DROPDOWNID=dropdown_id,
        ITEMS=items
    )

def navbar_drop_right(title: str, dropdown_id: str, items: str) -> str:
    '''A Navbar Item (not active)'''
    return HTMLSystem.part(
        "navbar/dropright",
        TITLE=title.title(),
        DROPDOWNID=dropdown_id,
        ITEMS=items
    )

def navbar_item(title: str, url: str) -> str:
    '''A Navbar Item (not active)'''
    return HTMLSystem.part(
        "navbar/item",
        TITLE=title.title(),
        URL=url.replace(" ", "/")
    )

def navbar_item_active(title: str) -> str:
    '''A Navbar Item (not active)'''
    return HTMLSystem.part(
        "navbar/itemactive",
        TITLE=title.title()
    )
