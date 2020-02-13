'''Script For the Admin System'''
import cherrypy
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE
from libs.authenticator import AUTHENTICATION
from libs.root_event import RootEvent
from libs.config.html.post_to_config import post_config_settings
from config_data import CONFIG

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
        index_page = CONFIG.html()
        javascript = "static/js/config.js"
        return self._template(index_page, javascript=javascript)


    @cherrypy.expose
    def users(self) -> str:
        '''Grab the users info'''
        AUTHENTICATION.check_auth()
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPRedirect(cherrypy.url().replace("/admin/users", "/"))
        data = AUTHENTICATION.get_users()
        users_html = ""
        for item in data:
            users_html += HTMLSystem.part(
                "admin/user",
                USERID=item['id'],
                USERNAME=item['username'],
                ADMINTRUE="checked" if item['is_admin'] else "",
                ADMINFALSE="" if item['is_admin'] else "checked"
            )
        return self._template(
            HTMLSystem.part(
                "admin/users",
                USERSHTML=users_html
            )
        )


    @cherrypy.expose
    def adduser(self, **kwargs) -> None: #TODO TO API
        '''Add user to system'''
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPRedirect(cherrypy.url().replace("/admin/adduser", "/"))
        username = kwargs.get("username", None)
        if username == "":
            username = None
        password = kwargs.get("password", None)
        if password == "":
            password = None
        is_admin = kwargs.get("is_admin", None)
        if is_admin == "True":
            is_admin = True
        elif is_admin == "False":
            is_admin = False
        else:
            is_admin = None
        if username is not None and password is not None and is_admin is not None:
            AUTHENTICATION.add_user(username, password, is_admin)
        raise cherrypy.HTTPRedirect(cherrypy.url().replace("adduser", "users"))


    @cherrypy.expose
    def updateuser(self, **kwargs) -> None: #TODO TO API
        '''update the user info'''
        if 'user_id' in kwargs:
            user_id = kwargs['user_id']
            if not AUTHENTICATION.is_admin():
                url = "/admin/updateuser/" + str(user_id) + "/"
                raise cherrypy.HTTPRedirect(cherrypy.url().replace(url, "/"))
            if 'delete' in kwargs:
                AUTHENTICATION.delete_user(user_id)
            elif 'update' in kwargs:
                username = kwargs.get("username", None)
                password = kwargs.get("password", None)
                if password == "":
                    password = None
                is_admin = kwargs.get("is_admin", None)
                AUTHENTICATION.update_user(user_id, username, password, is_admin)
        raise cherrypy.HTTPRedirect(cherrypy.url().replace("updateuser", "users"))


    @cherrypy.expose
    def reboot(self, url: str = "login") -> str: #TODO TO API
        '''Login Page'''
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPError(status=401)
        RootEvent.set_event("reboot")
        return self._template(HTMLSystem.part("reboot", PAGE=url), False)


    @cherrypy.expose
    def shutdown(self) -> str: #TODO TO API
        '''Login Page'''
        if not AUTHENTICATION.is_admin():
            raise cherrypy.HTTPError(status=401)
        RootEvent.set_event("shutdown")
        return self._template("Shuting Down Tackem...", False)
