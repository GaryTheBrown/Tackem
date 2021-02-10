'''Webserver'''
from typing import Optional
from data.config import CONFIG
from libs.httpd import Httpd
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE
class Webserver:
    '''Webserver'''
    __webserver = None

    @classmethod
    def load(cls) -> Optional[bool]:
        '''loads the webserver system'''
        if cls.__webserver is None:
            HTMLTEMPLATE.set_baseurl(CONFIG['webui']['baseurl'].value)
            cls.__webserver = Httpd()
            HTMLSystem.set_theme(CONFIG['webui']['theme'].value)
            return True
        return None

    @classmethod
    def delete(cls) -> bool:
        '''deletes the webserver'''
        if cls.__webserver is not None:
            cls.__webserver = None
            return True
        return False

    @classmethod
    def start(cls) -> bool:
        '''starts the webserver'''
        if cls.__webserver is not None:
            cls.__webserver.start()
            return True
        return False

    @classmethod
    def stop(cls) -> bool:
        '''stops the Webserver'''
        if cls.__webserver is not None:
            cls.__webserver.stop()
        return True

    @classmethod
    def restart(cls) -> bool:
        '''restart the Webserver'''
        return cls.__stop_webserver() and cls.__delete_webserver() \
            and cls.__load_webserver() and cls.__start_webserver()
