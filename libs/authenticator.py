'''Authentication system for all html pages listed'''
from typing import Union
import uuid
import hashlib
import cherrypy
from libs.database import Database
from libs.database.messages import SQLDelete, SQLInsert, SQLSelect, SQLTable
from libs.database.messages import SQLTableCountWhere, SQLUpdate
from libs.database.column import Column
from libs.database.table import Table
from libs.database.where import Where
from data.config import CONFIG

class Authentication:
    '''Authentication system for all html pages listed'''

    __db_info = Table(
        "authentication_info",
        1,
        Column("username", "text", not_null=True),
        Column("password", "text", not_null=True),
        Column("is_admin", "bit", not_null=True, default=False)
    )

    __login_url = CONFIG['webui']['baseurl'].value + "login?return_url="
    __temp_sessions = {}

    @classmethod
    def start(cls):
        '''Run starting commands need sql to run'''
        Database.call(SQLTable(cls.__db_info))

        msg = SQLTableCountWhere(cls.__db_info, Where("is_admin", True))
        Database.call(msg)
        if msg.return_data['COUNT(*)'] == 0:
            cls.__add_admin_account()

    @classmethod
    def __add_admin_account(cls):
        '''adds an admin account'''
        msg = SQLInsert(
            cls.__db_info,
            username="admin",
            password=cls.__password_encryption("admin"),
            is_admin=True
        )
        Database.call(msg)

    @classmethod
    def __password_encryption(cls, password: str) -> str:
        '''clear password to encrypted password'''
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @classmethod
    def login(
            cls,
            username: str,
            password: str,
            timeout: int,
            returnurl: str
    ) -> Union[bool, None]:
        '''Login Script'''
        if username == "" or password == "":
            return False

        msg = SQLSelect(cls.__db_info, Where("username", username))
        Database.call(msg)
        if msg.return_data['password'] != cls.__password_encryption(password):
            return False
        session_id = str(uuid.uuid1()).replace("-", "")
        del msg.return_data['password']
        msg.return_data['is_admin'] = msg.return_data['is_admin'] == "True"
        cls.__temp_sessions[session_id] = msg.return_data
        cherrypy.response.cookie['sessionid'] = session_id
        cherrypy.response.cookie['sessionid']['max-age'] = int(timeout) * 60
        if password == "admin":
            raise cherrypy.HTTPRedirect(
                cherrypy.url().replace("login", "password"))
        raise cherrypy.HTTPRedirect(
            cherrypy.url().replace("/login", returnurl))

    @classmethod
    def logout(cls):
        '''Logout Script'''
        session_id = cherrypy.request.cookie['sessionid'].value
        del cls.__temp_sessions[session_id]
        cherrypy.response.cookie['sessionid'] = session_id
        cherrypy.response.cookie['sessionid']['max-age'] = 0
        raise cherrypy.HTTPRedirect(cherrypy.url().replace("logout", "login"))

    @classmethod
    def check_auth(cls):
        '''Check authentication'''
        if 'sessionid' in cherrypy.request.cookie.keys():
            if cherrypy.request.cookie['sessionid'].value in cls.__temp_sessions:
                return
        raise cherrypy.HTTPRedirect(
            cls.__login_url + cherrypy.url(relative='server'))

    @classmethod
    def check_logged_in(cls) -> bool:
        '''Check if logged in'''
        if 'sessionid' in cherrypy.request.cookie.keys():
            if cherrypy.request.cookie['sessionid'].value in cls.__temp_sessions:
                return True
        return False

    @classmethod
    def is_admin(cls) -> bool:
        '''Returns if user is admin if logged in returns false if not logged in'''
        if 'sessionid' in cherrypy.request.cookie.keys():
            session_id = cherrypy.request.cookie['sessionid'].value
            if session_id in cls.__temp_sessions:
                return cls.__temp_sessions[session_id]['is_admin'] is True
        return False

    @classmethod
    def change_password(cls, password: str, new_password: str) -> bool:
        '''change the logged in users password'''
        if password == "" or new_password == "":
            return False
        if not 'sessionid' in cherrypy.request.cookie.keys():
            return False
        session_id = cherrypy.request.cookie['sessionid'].value
        user_id = cls.__temp_sessions[session_id]['id']
        msg1 = SQLSelect(cls.__db_info, Where("id", user_id))
        Database.call(msg1)
        if msg1.return_data['password'] != cls.__password_encryption(password):
            return False

        Database.call(
            SQLUpdate(
                cls.__db_info,
                Where("id", msg1.return_data['id']),
                password=cls.__password_encryption(new_password)
            )
        )
        return True

    @classmethod
    def add_user(cls, username: str, password: str, is_admin: bool):
        '''Add user to system'''
        user = {
            "username": username,
            "password": cls.__password_encryption(password),
            "is_admin": is_admin
        }
        msg1 = SQLTableCountWhere(cls.__db_info, Where("username", username))
        Database.call(msg1)
        if msg1.return_data['COUNT(*)'] == 0:
            msg2 = SQLInsert(cls.__db_info, **user)
            Database.call(msg2)

    @classmethod
    def delete_user(cls, user_id: int):
        '''Delete user from system'''
        Database.call(SQLDelete(cls.__db_info, Where("id", user_id)))

    @classmethod
    def get_users(cls):
        '''Grab the users info'''
        return_list = ["id", "username", "is_admin"]
        msg = SQLSelect(cls.__db_info, returns=return_list)
        Database.call(msg)
        for item in msg.return_data:
            item['is_admin'] = item['is_admin'] == "True"
        return msg.return_data

    @classmethod
    def update_user(
            cls,
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
            data['password'] = cls.__password_encryption(password)
        if isinstance(is_admin, bool) and is_admin != "":
            data['is_admin'] = is_admin

        Database.call(
            SQLUpdate(
                cls.__db_info,
                Where("id", user_id),
                **data
            )
        )

    @classmethod
    def clear_sessions(cls):
        '''clears the sessions and logs all the users out'''
        cls.__temp_sessions = {}
