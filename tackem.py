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
from libs.database import Database
from data.config import CONFIG

# TODO intergrate Libraries into main program
# is it going to be a single or multi instance?

# TODO Pull Ripper plugin back into the System with checks for programs to load system then checks
# on if drives exist and give the option of ripping locally or just giving ISO
# TODO Allow ripper to just accept ISOs instead if no drives in the machine.
# then we can create some api call to say there is a new ISO to work with,
# would need to check the process of getting info from the bluray for it's codes we are using.
# a seperate system for ripping drives should be created as another app.
# https://askubuntu.com/questions/147800/ripping-dvd-to-iso-accurately

# TODO NEED A TOOL FOR AUDIO ISO TO {MUSIC FILE}

# TODO need a way of having plugins require Other Plugins
# the plugin will auto download all required plugins
# these plugins should not allow you to enable them unless the required plugins are setup.
# Link to Library types allowed, all(*) or None.
# the plugin then needs a way of passing data to another plugin not through API.
# maybe a plugin message system.

# TODO UNIT TEST WHOLE SYSTEM, SELENIUM ON THE PAGES TOO.
# TODO SETUP GITHUB ACTIONS TO DO ALL THIS TESTING
# TODO the same for all plugins

class Tackem:
    '''main program entrance'''

    def __init__(self):
        self.__webserver = None

    def start(self):
        '''Start of the program'''
        print("LOADING PLUGINS...")
        TackemSystemAdmin().load_plugins()
        print("LOADING CONFIG...")
        CONFIG.load()
        print("LOADING DATABASE...")
        Database.setup_db()
        print("STARTING DATABASE...")
        Database.start_sql()
        print("STARTING AUTHENTICATOR...")
        AUTHENTICATION.start()
        print("STARTING LIBRARIES...")
        print("TODO")
        #if (Ripper):
        #   print("STARTING RIPPER...")
        print("LOADING SYSTEMS...")
        TackemSystemAdmin().load_systems()
        print("STARTING SYSTEMS...")
        TackemSystemAdmin().start_systems()
        print("LOADING WEBSERVICES...")
        self.__load_webserver()
        print("STARTING WEBSERVICES...")
        self.__start_webserver()
        print("TACKEM HAS STARTED")

    def stop(self):
        '''Stop commands'''
        print("STOPPING WEB SERVICES...")
        self.__stop_webserver()
        print("STOPPING SYSTEMS...")
        TackemSystemAdmin().stop_systems()
        #if (Ripper):
        #   print("STARTING RIPPER...")
        print("STOPPING LIBRARIES...")
        print("TODO")
        print("STOPPING DATABASE...")
        Database.stop_sql()

    def cleanup(self):
        '''Cleanup commands'''
        print("CLEANING UP...")
        self.__delete_webserver()
        TackemSystemAdmin().unload_systems()
        TackemSystemAdmin().unload_plugins()

    def shutdown(self):
        '''Shutdown commands'''
        self.stop()
        print("SAVING CONFIG FILE...")
        CONFIG.save()
        print("SHUTDOWN COMPLETED")

    def run(self):
        '''Looping function'''
        if not os.path.exists(PROGRAMCONFIGLOCATION):
            os.mkdir(PROGRAMCONFIGLOCATION)

        signal.signal(signal.SIGINT, ctrl_c) # Setup signal to watch for ctrl + c command
        self.start()
        while True:
            event, data = RootEvent.wait_and_get_event()

            if event is False:
                continue
            if event == "shutdown":
                self.shutdown()
                break
            if event == "reboot":
                self.shutdown()
                self.start()
                continue
            if event == "start_system":
                TackemSystemAdmin().load_system(data, len(data.split(" ")) == 2)
                TackemSystemAdmin().start_system(data)
                self.__restart_webserver()
                continue
            if event == "stop_system":
                TackemSystemAdmin().stop_system(data)
                TackemSystemAdmin().unload_system(data)
                self.__restart_webserver()
                continue

            print("Event Not Recognised Ignoring")
            continue

        self.cleanup()

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
        if self.__webserver is not None:
            self.__webserver.stop()
        return True

    def __restart_webserver(self) -> bool:
        '''restart the Webserver'''
        return self.__stop_webserver() and self.__delete_webserver() \
            and self.__load_webserver() and self.__start_webserver()

# Catching the ctrl + c event and doing a clean shutdown
def ctrl_c(_, __):
    '''Function to call once ctrl + c is pressed'''
    print(" caught Shutting Down Cleanly...")
    RootEvent.set_event("shutdown")

if __name__ == "__main__":
    Tackem().run()
    signal.signal(signal.SIGINT, False)
