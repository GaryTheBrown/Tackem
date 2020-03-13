'''Authentication system for all html pages listed'''
from typing import Union
import uuid
import hashlib
import cherrypy
from libs.sql import Database
from libs.sql.column import Column
from config_data import CONFIG


class Authentication:
    '''Authentication system for all html pages listed'''

    __db_info = {
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

    __temp_sessions = {}

    def __init__(self):
        self.__login_url = CONFIG['webui']['baseurl'].value + \
            "login?return_url="

    def start(self) -> None:
        '''Run starting commands need sql to run'''
        Database.sql().table_checks("Auth", self.__db_info)
        if Database.sql().count("Auth", self.__db_info['name']) == 0:
            self.__add_admin_account()
        elif Database.sql().count_where("Auth", self.__db_info['name'], {"is_admin": True}) == 0:
            self.__add_admin_account()

    def __add_admin_account(self) -> None:
        '''adds an admin account'''
        user = {
            "username": "admin",
            "password": self.__password_encryption("admin"),
            "is_admin": True
        }
        Database.sql().insert("Auth", self.__db_info['name'], user)

    def __password_encryption(self, password: str) -> str:
        '''clear password to encrypted password'''
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def login(
        self,
        username: str,
        password: str,
        timeout: int,
        returnurl: str
    ) -> Union[bool, None]:
        '''Login Script'''
        if username == "" or password == "":
            return False
        data = Database.sql().select(
            "Auth", self.__db_info['name'], {"username": username})[0]
        if data['password'] != self.__password_encryption(password):
            return False
        session_id = str(uuid.uuid1()).replace("-", "")
        del data['password']
        data['is_admin'] = data['is_admin'] == "True"
        self.__temp_sessions[session_id] = data
        cherrypy.response.cookie['sessionid'] = session_id
        cherrypy.response.cookie['sessionid']['max-age'] = int(timeout) * 60
        if password == "admin":
            raise cherrypy.HTTPRedirect(
                cherrypy.url().replace("login", "password"))
        raise cherrypy.HTTPRedirect(
            cherrypy.url().replace("/login", returnurl))

    def logout(self) -> None:
        '''Logout Script'''
        session_id = cherrypy.request.cookie['sessionid'].value
        del self.__temp_sessions[session_id]
        cherrypy.response.cookie['sessionid'] = session_id
        cherrypy.response.cookie['sessionid']['max-age'] = 0
        raise cherrypy.HTTPRedirect(cherrypy.url().replace("logout", "login"))

    def check_auth(self) -> None:
        '''Check authentication'''
        if 'sessionid' in cherrypy.request.cookie.keys():
            if cherrypy.request.cookie['sessionid'].value in self.__temp_sessions:
                return
        raise cherrypy.HTTPRedirect(
            self.__login_url + cherrypy.url(relative='server'))

    def check_logged_in(self) -> bool:
        '''Check if logged in'''
        if 'sessionid' in cherrypy.request.cookie.keys():
            if cherrypy.request.cookie['sessionid'].value in self.__temp_sessions:
                return True
        return False

    def is_admin(self) -> bool:
        '''Returns if user is admin if logged in returns false if not logged in'''
        if 'sessionid' in cherrypy.request.cookie.keys():
            session_id = cherrypy.request.cookie['sessionid'].value
            if session_id in self.__temp_sessions:
                return self.__temp_sessions[session_id]['is_admin'] is True
        return False

    def change_password(self, password: str, new_password: str) -> bool:
        '''change the logged in users password'''
        if password == "" or new_password == "":
            return False
        if not 'sessionid' in cherrypy.request.cookie.keys():
            return False
        session_id = cherrypy.request.cookie['sessionid'].value
        user_id = self.__temp_sessions[session_id]['id']
        data = Database.sql().select(
            "Auth", self.__db_info['name'], {"id": user_id})[0]
        if data['password'] != self.__password_encryption(password):
            return False
        Database.sql().update("Auth", self.__db_info['name'], data['id'],
                              {"password": self.__password_encryption(new_password)})
        return True

    def add_user(self, username: str, password: str, is_admin: bool) -> None:
        '''Add user to system'''
        user = {
            "username": username,
            "password": self.__password_encryption(password),
            "is_admin": is_admin
        }
        if Database.sql().count_where("Auth", self.__db_info['name'], {"username": username}) == 0:
            Database.sql().insert("Auth", self.__db_info['name'], user)

    def delete_user(self, user_id: int) -> None:
        '''Delete user from system'''
        Database.sql().delete_row("Auth", self.__db_info['name'], user_id)

    def get_users(self):
        '''Grab the users info'''
        return_list = ["id", "username", "is_admin"]
        data = Database.sql().select(
            "Auth", self.__db_info['name'], list_of_returns=return_list)
        for item in data:
            item['is_admin'] = item['is_admin'] == "True"
        return data

    def update_user(
        self,
        user_id: int,
        username: Union[str, None] = None,
        password: Union[str, None] = None,
        is_admin: bool = None
    ) -> None:
        '''update the user info'''
        data = {}
        if isinstance(username, str) and username != "":
            data['username'] = username
        if isinstance(password, str) and password != "":
            data['password'] = self.__password_encryption(password)
        if isinstance(is_admin, bool) and is_admin != "":
            data['is_admin'] = is_admin
        Database.sql().update("Auth", self.__db_info['name'], user_id, data)

    def clear_sessions(self) -> None:
        '''clears the sessions and logs all the users out'''
        self.__temp_sessions = {}


AUTHENTICATION = Authentication()
