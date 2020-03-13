'''Start Point Of Program'''
# https://docs.cherrypy.org/en/latest/tutorials.html
import os
import os.path
import signal
from typing import Union
from system.admin import TackemSystemAdmin
from libs.startup_arguments import PROGRAMCONFIGLOCATION
from libs.root_event import RootEventMaster as RootEvent
from libs.httpd import Httpd
from libs.html_system import HTMLSystem
from libs.html_template import HTMLTEMPLATE
from libs.authenticator import AUTHENTICATION
from libs.sql import Database
from config_data import CONFIG

# TODO FIX CONFIG MULTI ADD
# TODO fix the plugin downloader to working


class Tackem:
    '''main program entrance'''

    def __init__(self):
        self.__webserver = None

    def start(self) -> None:
        '''Start of the program'''
        print("LOADING PLUGINS...")
        TackemSystemAdmin().import_plugins()
        print("LOADING CONFIG...")
        CONFIG.load()
        print("LOADING DATABASE...")
        Database.setup_db()
        print("STARTING DATABASE...")
        Database.start_sql()
        print("STARTING AUTHENTICATOR...")
        AUTHENTICATION.start()
        print("LOADING SYSTEMS...")
        TackemSystemAdmin().load_systems()
        print("STARTING SYSTEMS...")
        TackemSystemAdmin().start_systems()
        print("LOADING WEBSERVICES...")
        self.__load_webserver()
        print("STARTING WEBSERVICES...")
        self.__start_webserver()
        print("TACKEM HAS STARTED")

    def stop(self) -> None:
        '''Stop commands'''
        print("STOPPING WEB SERVICES...")
        self.__stop_webserver()
        print("STOPPING SYSTEMS...")
        TackemSystemAdmin().stop_systems()
        print("STOPPING DATABASE...")
        Database.stop_sql()

    def cleanup(self) -> None:
        '''Cleanup commands'''
        print("CLEANING UP...")
        self.__delete_webserver()
        TackemSystemAdmin().remove_systems()
        TackemSystemAdmin().remove_plugins()

    def shutdown(self) -> None:
        '''Shutdown commands'''
        self.stop()
        print("SAVING CONFIG FILE...")
        CONFIG.save()
        print("SHUTDOWN COMPLETED")

    def run(self) -> None:
        '''Looping function'''

        # First check if home folder exists (useable to run first time script)
        if not os.path.exists(PROGRAMCONFIGLOCATION):
            os.mkdir(PROGRAMCONFIGLOCATION)

        # Setup signal to watch for ctrl + c command
        signal.signal(signal.SIGINT, ctrl_c)
        self.start()
        while True:
            event_type = RootEvent.wait_and_get_event()

            if event_type is False:
                continue
            if event_type == "shutdown":
                self.shutdown()
                break
            if event_type == "reboot":
                self.shutdown()
                self.start()
            else:
                print("Event Not Recognised Ignoring")
                continue

        self.cleanup()

    # Webserver Methods

    def __load_webserver(self) -> Union[bool, None]:
        '''loads the webserver system'''
        if self.__webserver is None:
            HTMLTEMPLATE.set_baseurl(CONFIG['webui']['baseurl'].value)
            self.__webserver = Httpd()
            HTMLSystem.set_theme(CONFIG['webui']['theme'].value)
            return True
        return None

    def __delete_webserver(self) -> bool:
        '''deletes the webserver'''
        if self.__webserver is not None:
            self.__webserver = None
            return True
        return False

    def __start_webserver(self) -> bool:
        '''starts the webserver'''
        if self.__webserver is not None:
            self.__webserver.start()
        return True

    def __stop_webserver(self) -> bool:
        '''stops the Webserver'''
        # if CONFIG['webui']['disabled'].value:
        #     return False
        if self.__webserver is not None:
            self.__webserver.stop()
        return True


##############################################
# Catching the ctrl + c event and doing a clean shutdown
def ctrl_c(_, __):
    '''Function to call once ctrl + c is pressed'''
    print(" caught Shutting Down Cleanly...")
    RootEvent.set_event("shutdown")
##############################################


if __name__ == "__main__":
    Tackem().run()
    signal.signal(signal.SIGINT, False)
