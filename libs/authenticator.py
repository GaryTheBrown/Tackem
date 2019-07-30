'''Authentication system for all html pages listed'''
import uuid
import hashlib
import cherrypy
from libs.sql.column import Column
from system.root import TackemSystemRoot

class Authentication:
    '''Authentication system for all html pages listed'''

    _db_info = {
        "name": "Authentication_info",
        "data":
            [
                Column("id", "integer", primary_key=True, not_null=True),
                Column("username", "text", not_null=True),
                Column("password", "text", not_null=True),
                Column("is_admin", "bit", not_null=True, default=False),
            ],
        "version": 1
    }

    _temp_sessions = {}

    def __init__(self):
        self._tackem_system = TackemSystemRoot('scraper')
        self._login_url = self._tackem_system.get_config(["webui", "baseurl"], "/")
        self._login_url += "login?return_url="

    def start(self):
        '''Run starting commands need sql to run'''
        self._tackem_system.get_sql().table_checks("Auth", self._db_info)
        if self._tackem_system.get_sql().count("Auth", self._db_info['name']) == 0:
            self._add_admin_account()
        elif self._tackem_system.get_sql().count_where("Auth", self._db_info['name'],
                                                       {"is_admin":True}) == 0:
            self._add_admin_account()

    def _add_admin_account(self):
        '''adds an admin account'''
        user = {
            "username": "admin",
            "password": self._password_encryption("admin"),
            "is_admin": True
        }
        self._tackem_system.get_sql().insert("Auth", self._db_info['name'], user)

    def _password_encryption(self, password):
        '''clear password to encrypted password'''
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    def enabled(self):
        '''is authentication enabled'''
        return self._tackem_system.config()['enabled']

    def login(self, username, password, timeout, returnurl):
        '''Login Script'''
        if username == "" or password == "":
            return False
        data = self._tackem_system.get_sql().select("Auth", self._db_info['name'],
                                                    {"username":username})[0]
        if data['password'] != self._password_encryption(password):
            return False
        session_id = str(uuid.uuid1()).replace("-", "")
        del data['password']
        data['is_admin'] = data['is_admin'] == "True"
        self._temp_sessions[session_id] = data
        cherrypy.response.cookie['sessionid'] = session_id
        cherrypy.response.cookie['sessionid']['max-age'] = int(timeout) * 60
        if password == "admin":
            raise cherrypy.HTTPRedirect(cherrypy.url().replace("login", "password"))
        raise cherrypy.HTTPRedirect(cherrypy.url().replace("/login", returnurl))

    def logout(self):
        '''Logout Script'''
        session_id = cherrypy.request.cookie['sessionid'].value
        del self._temp_sessions[session_id]
        cherrypy.response.cookie['sessionid'] = session_id
        cherrypy.response.cookie['sessionid']['max-age'] = 0
        raise cherrypy.HTTPRedirect(cherrypy.url().replace("logout", "login"))

    def check_auth(self):
        '''Check authentication'''
        if not self._tackem_system.config()['enabled']:
            return
        if 'sessionid' in cherrypy.request.cookie.keys():
            if cherrypy.request.cookie['sessionid'].value in self._temp_sessions:
                return
        raise cherrypy.HTTPRedirect(self._login_url + cherrypy.url(relative='server'))

    def check_logged_in(self):
        '''Check if logged in'''
        if not self._tackem_system.config()['enabled']:
            return
        if 'sessionid' in cherrypy.request.cookie.keys():
            if cherrypy.request.cookie['sessionid'].value in self._temp_sessions:
                return True
        return False

    def is_admin(self):
        '''Returns if user is admin if logged in returns false if not logged in'''
        if not self._tackem_system.config()['enabled']:
            return True
        if 'sessionid' in cherrypy.request.cookie.keys():
            session_id = cherrypy.request.cookie['sessionid'].value
            if session_id in self._temp_sessions:
                return self._temp_sessions[session_id]['is_admin'] is True
        return False

    def change_password(self, password, new_password):
        '''change the logged in users password'''
        if password == "" or new_password == "":
            return False
        if not 'sessionid' in cherrypy.request.cookie.keys():
            return False
        session_id = cherrypy.request.cookie['sessionid'].value
        user_id = self._temp_sessions[session_id]['id']
        data = self._tackem_system.get_sql().select("Auth", self._db_info['name'],
                                                    {"id":user_id})[0]
        if data['password'] != self._password_encryption(password):
            return False
        self._tackem_system.get_sql().update("Auth", self._db_info['name'], data['id'],
                                             {"password": self._password_encryption(new_password)})
        return True

    def add_user(self, username, password, is_admin):
        '''Add user to system'''
        user = {
            "username": username,
            "password": self._password_encryption(password),
            "is_admin": is_admin
        }
        if self._tackem_system.get_sql().count_where("Auth", self._db_info['name'],
                                                     {"username":username}) == 0:
            self._tackem_system.get_sql().insert("Auth", self._db_info['name'], user)

    def delete_user(self, user_id):
        '''Delete user from system'''
        self._tackem_system.get_sql().delete_row("Auth", self._db_info['name'], user_id)

    def get_users(self):
        '''Grab the users info'''
        return_list = ["id", "username", "is_admin"]
        data = self._tackem_system.get_sql().select("Auth", self._db_info['name'],
                                                    list_of_returns=return_list)
        for item in data:
            item['is_admin'] = item['is_admin'] == "True"
        return data

    def update_user(self, user_id, username=None, password=None, is_admin=None):
        '''update the user info'''
        data = {}
        if isinstance(username, str):
            data['username'] = username
        if isinstance(password, str):
            data['password'] = self._password_encryption(password)
        if isinstance(is_admin, bool):
            data['is_admin'] = is_admin
        self._tackem_system.get_sql().update("Auth", self._db_info['name'], user_id, data)

    def clear_sessions(self):
        '''clears the sessions and logs all the users out'''
        self._temp_sessions = {}
