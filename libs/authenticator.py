"""Authentication system for all html pages listed"""
import hashlib
import random
import uuid
from typing import Union

import cherrypy

from data.config import CONFIG
from libs.database import Database
from libs.database.column import Column
from libs.database.messages.delete import SQLDelete
from libs.database.messages.insert import SQLInsert
from libs.database.messages.select import SQLSelect
from libs.database.messages.table import SQLTable
from libs.database.messages.table_count_where import SQLTableCountWhere
from libs.database.messages.update import SQLUpdate
from libs.database.table import Table
from libs.database.where import Where
from libs.file import File


class Authentication:
    """Authentication system for all html pages listed"""

    __db_info = Table(
        "authentication_info",
        1,
        Column("username", "text", not_null=True),
        Column("password", "text", not_null=True),
        Column("is_admin", "bit", not_null=True, default=False),
    )

    __login_url = CONFIG["webui"]["baseurl"].value + "login?return_url="
    __temp_sessions = {}

    @classmethod
    def start(cls):
        """Run starting commands need sql to run"""
        Database.call(SQLTable(cls.__db_info))

        msg = SQLTableCountWhere(cls.__db_info, Where("is_admin", True))
        Database.call(msg)
        if msg.return_data["COUNT(*)"] == 0:
            cls.__add_admin_account()

    @classmethod
    def __add_admin_account(cls):
        """adds an admin account"""
        password = cls.generate_password()
        with open(File.location("adminpasssword"), "w") as f:
            f.write(password)

        msg = SQLInsert(
            cls.__db_info,
            username="admin",
            password=cls.__password_encryption(password),
            is_admin=True,
        )
        Database.call(msg)

    @classmethod
    def __password_encryption(cls, password: str) -> str:
        """clear password to encrypted password"""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @classmethod
    def generate_password(cls, length: int = 16) -> str:
        """Generates a random password"""

        def rchar():
            rnd = random.SystemRandom()
            return rnd.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")

        password = rchar()
        for _ in range(length + 1):
            password += rchar()
        return password

    @classmethod
    def login(cls, username: str, password: str, timeout: int, returnurl: str) -> Union[bool, None]:
        """Login Script"""
        if not username or not password:
            return False

        msg = SQLSelect(cls.__db_info, Where("username", username))
        Database.call(msg)
        if msg.return_data["password"] != cls.__password_encryption(password):
            return False
        session_id = str(uuid.uuid1()).replace("-", "")
        del msg.return_data["password"]
        msg.return_data["is_admin"] = msg.return_data["is_admin"] == "True"
        cls.__temp_sessions[session_id] = msg.return_data
        cherrypy.response.cookie["sessionid"] = session_id
        cherrypy.response.cookie["sessionid"]["max-age"] = int(timeout) * 60
        raise cherrypy.HTTPRedirect(cherrypy.url().replace("/login", returnurl))

    @classmethod
    def logout(cls):
        """Logout Script"""
        session_id = cherrypy.request.cookie["sessionid"].value
        del cls.__temp_sessions[session_id]
        cherrypy.response.cookie["sessionid"] = session_id
        cherrypy.response.cookie["sessionid"]["max-age"] = 0
        raise cherrypy.HTTPRedirect(cherrypy.url().replace("logout", "login"))

    @classmethod
    def check_auth(cls):
        """Check authentication"""
        if "sessionid" in cherrypy.request.cookie.keys():
            if cherrypy.request.cookie["sessionid"].value in cls.__temp_sessions:
                return
        raise cherrypy.HTTPRedirect(cls.__login_url + cherrypy.url(relative="server"))

    @classmethod
    def check_logged_in(cls) -> bool:
        """Check if logged in"""
        if "sessionid" in cherrypy.request.cookie.keys():
            if cherrypy.request.cookie["sessionid"].value in cls.__temp_sessions:
                return True
        return False

    @classmethod
    def is_admin(cls) -> bool:
        """Returns if user is admin if logged in returns false if not logged in"""
        if "sessionid" in cherrypy.request.cookie.keys():
            session_id = cherrypy.request.cookie["sessionid"].value
            if session_id in cls.__temp_sessions:
                return cls.__temp_sessions[session_id]["is_admin"] is True
        return False

    @classmethod
    def change_password(cls, password: str, new_password: str) -> bool:
        """change the logged in users password"""
        if not password or not new_password:
            return False
        if "sessionid" not in cherrypy.request.cookie.keys():
            return False
        session_id = cherrypy.request.cookie["sessionid"].value
        user_id = cls.__temp_sessions[session_id]["id"]
        msg1 = SQLSelect(cls.__db_info, Where("id", user_id))
        Database.call(msg1)
        if msg1.return_data["password"] != cls.__password_encryption(password):
            return False

        Database.call(
            SQLUpdate(
                cls.__db_info,
                Where("id", msg1.return_data["id"]),
                password=cls.__password_encryption(new_password),
            )
        )
        return True

    @classmethod
    def add_user(cls, username: str, password: str, is_admin: bool):
        """Add user to system"""
        user = {
            "username": username,
            "password": cls.__password_encryption(password),
            "is_admin": is_admin,
        }
        msg1 = SQLTableCountWhere(cls.__db_info, Where("username", username))
        Database.call(msg1)
        if msg1.return_data["COUNT(*)"] == 0:
            msg2 = SQLInsert(cls.__db_info, **user)
            Database.call(msg2)

    @classmethod
    def delete_user(cls, user_id: int):
        """Delete user from system"""
        Database.call(SQLDelete(cls.__db_info, Where("id", user_id)))

    @classmethod
    def get_users(cls):
        """Grab the users info"""
        return_list = ["id", "username", "is_admin"]
        msg = SQLSelect(cls.__db_info, returns=return_list)
        Database.call(msg)
        if isinstance(msg.return_data, dict):
            msg.return_data["is_admin"] = msg.return_data["is_admin"] == "True"
        elif isinstance(msg.return_data, list):
            for item in msg.return_data:
                item["is_admin"] = item["is_admin"] == "True"
        return msg.return_data

    @classmethod
    def update_user(
        cls,
        user_id: int,
        username: Union[str, None] = None,
        password: Union[str, None] = None,
        is_admin: bool = None,
    ):
        """update the user info"""
        data = {}
        if isinstance(username, str) and len(username) > 0:
            data["username"] = username
        if isinstance(password, str) and len(password) > 0:
            data["password"] = cls.__password_encryption(password)
        if isinstance(is_admin, bool):
            data["is_admin"] = is_admin

        Database.call(SQLUpdate(cls.__db_info, Where("id", user_id), **data))

    @classmethod
    def clear_sessions(cls):
        """clears the sessions and logs all the users out"""
        cls.__temp_sessions = {}
