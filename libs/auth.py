"""Auth system for all html pages listed"""
import hashlib
import random
import uuid
from typing import Union

import cherrypy

from config import CONFIG
from database.user import User
from libs.file import File


class Auth:
    """Auth system for all html pages listed"""

    GUEST: int = 0
    USER: int = 1
    ADMIN: int = 2

    TYPESTR = ["Guest", "User", "Admin"]

    __login_url = CONFIG["webui"]["baseurl"].value + "login?return_url="
    __temp_sessions = {}

    @classmethod
    def start(cls):
        """Run starting commands need sql to run"""

        User.table_setup()

        if User.do_select().where(User.is_admin == True).count() == 0:  # noqa E712
            password = cls.generate_password()
            with open(File.location("adminpasssword"), "w") as f:
                f.write(password)

            User.insert(
                username="admin", password=cls.__password_encryption(password), is_admin=True
            ).execute()

    @staticmethod
    def __password_encryption(password: str) -> str:
        """clear password to encrypted password"""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def generate_password(length: int = 16) -> str:
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
        enc_pass = cls.__password_encryption(password)
        user = (
            User.do_select()
            .where(User.username == username, User.password == enc_pass)
            .get_or_none()
        )
        if user is None:
            return False
        session_id = str(uuid.uuid1()).replace("-", "")
        cls.__temp_sessions[session_id] = user.id
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
    def check_logged_in(cls) -> int:
        """Check if logged in"""
        if "sessionid" in cherrypy.request.cookie.keys():
            sessionid = cherrypy.request.cookie["sessionid"].value
            if sessionid in cls.__temp_sessions:
                user: User = User.get_by_id(cls.__temp_sessions[sessionid])
                is_admin = user.is_admin
                if is_admin:
                    return cls.ADMIN
                return cls.USER
        return cls.GUEST

    @classmethod
    def get_logged_in_userid(cls) -> int:
        """Check if logged in"""
        if "sessionid" in cherrypy.request.cookie.keys():
            if cherrypy.request.cookie["sessionid"].value in cls.__temp_sessions:
                return cls.__temp_sessions[cherrypy.request.cookie["sessionid"].value]

    @classmethod
    def check_auth(cls):
        """Check auth"""
        if cls.check_logged_in() == cls.GUEST:
            raise cherrypy.HTTPRedirect(cls.__login_url + cherrypy.url(relative="server"))

    @classmethod
    def is_admin(cls):
        """Returns if user is admin if logged in returns false if not logged in"""
        if cls.check_logged_in() != cls.ADMIN:
            raise cherrypy.HTTPError(status=401)

    @classmethod
    def change_password(cls, password: str, new_password: str) -> bool:
        """change the logged in users password"""
        if not password or not new_password:
            return False
        if "sessionid" not in cherrypy.request.cookie.keys():
            return False

        session_id = cherrypy.request.cookie["sessionid"].value
        user: User = User.get_by_id(cls.__temp_sessions[session_id])

        if user.password != cls.__password_encryption(password):
            return False

        user.password = cls.__password_encryption(new_password)
        user.save()
        return True

    @classmethod
    def add_user(cls, username: str, password: str, is_admin: bool) -> bool:
        """Add user to system"""
        user = User()
        user.username = username
        user.password = cls.__password_encryption(password)
        user.is_admin = is_admin
        return user.save() == 1

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Delete user from system"""
        return User.do_delete().where(User.id == user_id).execute() == 1

    @staticmethod
    def get_users() -> list:
        """Grab the users info"""
        return User.do_select(User.id, User.username, User.is_admin)

    @classmethod
    def update_user(
        cls,
        user_id: int,
        username: Union[str, None] = None,
        password: Union[str, None] = None,
        is_admin: bool = None,
    ) -> bool:
        """update the user info"""
        if cls.check_logged_in() != cls.ADMIN and cls.get_logged_in_userid() != user_id:
            return False

        user = User.get_by_id(user_id)

        if isinstance(username, str) and len(username) > 0:
            user.username = username
        if isinstance(password, str) and len(password) > 0:
            user.password = cls.__password_encryption(password)
        if isinstance(is_admin, bool):
            user.is_admin = is_admin
        return user.save() == 1

    @classmethod
    def clear_sessions(cls):
        """clears the sessions and logs all the users out"""
        cls.__temp_sessions = {}
