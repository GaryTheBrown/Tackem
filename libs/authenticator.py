'''Authentication system for all html pages listed'''
from typing import Union
import uuid
import hashlib
import cherrypy
from libs.database import Database
from libs.database.messages import SQLDelete, SQLInsert, SQLSelect, SQLTable, SQLTableCount
from libs.database.messages import SQLTableCountWhere, SQLUpdate
from libs.database.column import Column
from libs.database.table import Table
from libs.database.where import Where
from config_data import CONFIG

class Authentication:
    '''Authentication system for all html pages listed'''

    __db_info = Table(
        "authentication_info",
        1,
        Column("username", "text", not_null=True),
        Column("password", "text", not_null=True),
        Column("is_admin", "bit", not_null=True, default=False)
    )

    __temp_sessions = {}

    def __init__(self):
        self.__login_url = CONFIG['webui']['baseurl'].value + \
            "login?return_url="

    def start(self):
        '''Run starting commands need sql to run'''
        Database.call(SQLTable(self.__db_info))
        msg1 = SQLTableCount(self.__db_info.name())
        Database.call(msg1)
        msg2 = SQLTableCountWhere(self.__db_info.name(), Where("is_admin", True))
        Database.call(msg2)
        if msg1.return_data['COUNT(*)'] == 0:
            self.__add_admin_account()
        elif msg2.return_data['COUNT(*)'] == 0:
            self.__add_admin_account()

    def __add_admin_account(self):
        '''adds an admin account'''
        msg = SQLInsert(
            self.__db_info.name(),
            username="admin",
            password=self.__password_encryption("admin"),
            is_admin=True
        )
        Database.call(msg)

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

        msg = SQLSelect(self.__db_info.name(), Where("username", username))
        Database.call(msg)
        if msg.return_data['password'] != self.__password_encryption(password):
            return False
        session_id = str(uuid.uuid1()).replace("-", "")
        del msg.return_data['password']
        msg.return_data['is_admin'] = msg.return_data['is_admin'] == "True"
        self.__temp_sessions[session_id] = msg.return_data
        cherrypy.response.cookie['sessionid'] = session_id
        cherrypy.response.cookie['sessionid']['max-age'] = int(timeout) * 60
        if password == "admin":
            raise cherrypy.HTTPRedirect(
                cherrypy.url().replace("login", "password"))
        raise cherrypy.HTTPRedirect(
            cherrypy.url().replace("/login", returnurl))

    def logout(self):
        '''Logout Script'''
        session_id = cherrypy.request.cookie['sessionid'].value
        del self.__temp_sessions[session_id]
        cherrypy.response.cookie['sessionid'] = session_id
        cherrypy.response.cookie['sessionid']['max-age'] = 0
        raise cherrypy.HTTPRedirect(cherrypy.url().replace("logout", "login"))

    def check_auth(self):
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
        msg1 = SQLSelect(self.__db_info.name(), Where("id", user_id))
        Database.call(msg1)
        print(msg1.return_data)
        if msg1.return_data['password'] != self.__password_encryption(password):
            return False

        Database.call(
            SQLUpdate(
                self.__db_info.name(),
                Where("id", msg1.return_data['id']),
                password=self.__password_encryption(new_password)
            )
        )
        return True

    def add_user(self, username: str, password: str, is_admin: bool):
        '''Add user to system'''
        user = {
            "username": username,
            "password": self.__password_encryption(password),
            "is_admin": is_admin
        }
        msg1 = SQLTableCountWhere(self.__db_info.name(), Where("username", username))
        Database.call(msg1)
        if msg1.return_data['COUNT(*)'] == 0:
            msg2 = SQLInsert(self.__db_info.name(), **user)
            Database.call(msg2)

    def delete_user(self, user_id: int):
        '''Delete user from system'''
        Database.call(SQLDelete(self.__db_info.name(), Where("id", user_id)))

    def get_users(self):
        '''Grab the users info'''
        return_list = ["id", "username", "is_admin"]
        msg = SQLSelect(self.__db_info.name(), returns=return_list)
        Database.call(msg)
        for item in msg.return_data:
            item['is_admin'] = item['is_admin'] == "True"
        return msg.return_data

    def update_user(
            self,
            user_id: int,
            username: Union[str, None] = None,
            password: Union[str, None] = None,
            is_admin: bool = None
    ):
        '''update the user info'''
        data = {}
        if isinstance(username, str) and username != "":
            data['username'] = username
        if isinstance(password, str) and password != "":
            data['password'] = self.__password_encryption(password)
        if isinstance(is_admin, bool) and is_admin != "":
            data['is_admin'] = is_admin

        Database.call(
            SQLUpdate(
                self.__db_info.name(),
                Where("id", user_id),
                **data
            )
        )

    def clear_sessions(self):
        '''clears the sessions and logs all the users out'''
        self.__temp_sessions = {}

AUTHENTICATION = Authentication()
