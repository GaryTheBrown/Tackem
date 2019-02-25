'''Script For the Admin System'''
import cherrypy
from libs import html_parts
from libs.html_template import HTMLTEMPLATE

class Admin(HTMLTEMPLATE):
    '''Admin'''

    @cherrypy.expose
    def users(self):
        '''Grab the users info'''
        self._auth.check_auth()
        if not self._auth.is_admin():
            raise cherrypy.HTTPRedirect(cherrypy.url().replace("/admin/users", "/"))
        data = self._auth.get_users()
        users_html = ""
        for item in data:
            users_html += html_parts.user_page(item['id'], item['username'], item['is_admin'])
        users_page_html = html_parts.users_page(users_html)
        return self._template(users_page_html)

    @cherrypy.expose
    def adduser(self, **kwargs):
        '''Add user to system'''
        if not self._auth.is_admin():
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
            self._auth.add_user(username, password, is_admin)
        raise cherrypy.HTTPRedirect(cherrypy.url().replace("adduser", "users"))

    @cherrypy.expose
    def updateuser(self, **kwargs):
        '''update the user info'''
        if 'user_id' in kwargs:
            user_id = kwargs['user_id']
            if not self._auth.is_admin():
                url = "/admin/updateuser/" + str(user_id) + "/"
                raise cherrypy.HTTPRedirect(cherrypy.url().replace(url, "/"))
            if 'delete' in kwargs:
                self._auth.delete_user(user_id)
            elif 'update' in kwargs:
                username = kwargs.get("username", None)
                password = kwargs.get("password", None)
                if password == "":
                    password = None
                is_admin = kwargs.get("is_admin", None)
                self._auth.update_user(user_id, username, password, is_admin)
        raise cherrypy.HTTPRedirect(cherrypy.url().replace("updateuser", "users"))
