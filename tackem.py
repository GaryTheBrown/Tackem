'''Start Point Of Program'''
#https://docs.cherrypy.org/en/latest/tutorials.html
import os
import os.path
import signal
from libs.startup_arguments import ARGS
from libs.root_event import RootEventMaster as RootEvent
from libs.httpd import Httpd
from system.admin import TackemSystemAdmin

class Tackem:
    '''main program entrance'''
    def __init__(self):
        self.__webserver = None

    def start(self):
        '''Start of the program'''
        print("LOADING PLUGINS...")
        TackemSystemAdmin().load_plugins()
        print("LOADING CONFIG...")
        TackemSystemAdmin().load_plugin_cfgs()
        TackemSystemAdmin().load_config()

        if not TackemSystemAdmin().get_config(['firstrun'], True):
            print("LOADING DATABASE...")
            TackemSystemAdmin().load_sql()
            print("STARTING DATABASE...")
            TackemSystemAdmin().start_sql()
            print("LOADING MUSICBRAINZ...")
            TackemSystemAdmin().load_musicbrainz()
            print("LOADING AUTHENTICATOR...")
            TackemSystemAdmin().load_auth()
            print("STARTING AUTHENTICATOR...")
            TackemSystemAdmin().start_auth()
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
        if not TackemSystemAdmin().get_config(['firstrun'], True):
            print("STOPPING SYSTEMS...")
            TackemSystemAdmin().stop_systems()
            print("STOPPING DATABASE...")
            TackemSystemAdmin().stop_sql()

    def cleanup(self):
        '''Cleanup commands'''
        print("CLEANING UP...")
        self.__delete_webserver()
        TackemSystemAdmin().delete_systems()
        TackemSystemAdmin().delete_sql()
        TackemSystemAdmin().delete_plugin_cfgs()
        TackemSystemAdmin().delete_plugins()
        TackemSystemAdmin().delete_musicbrainz()
        TackemSystemAdmin().delete_auth()
        TackemSystemAdmin().delete_config()


    def shutdown(self):
        '''Shutdown commands'''
        self.stop()
        print("SAVING CONFIG FILE...")
        TackemSystemAdmin().write_config_to_disk()
        print("SHUTDOWN COMPLETED")

    def run(self):
        '''Looping function'''

        #First check if home folder exists (useable to run first time script)
        if not os.path.exists(ARGS.home):
            os.mkdir(ARGS.home)

        #Setup signal to watch for ctrl + c command
        signal.signal(signal.SIGINT, ctrl_c)

        self.start()
        while True:
            event_type = RootEvent.wait_and_get_event()

            if event_type is False:
                continue
            elif event_type == "shutdown":
                self.shutdown()
                self.cleanup()
                break
            elif event_type == "reboot":
                self.shutdown()
                self.start()
            else:
                print("Event Not Recognised Ignoring")
                continue

        self.cleanup()

    #Webserver Methods
    def __load_webserver(self):
        '''loads the webserver system'''
        if not TackemSystemAdmin().get_config(['api', 'enabled'], True):
            return False
        if TackemSystemAdmin().get_config(['webui', 'disabled'], False):
            return False
        if self.__webserver is None:
            self.__webserver = Httpd()
            return True
        return None

    def __delete_webserver(self):
        '''deletes the webserver'''
        if self.__webserver is not None:
            self.__webserver = None

    def __start_webserver(self):
        '''starts the webserver'''
        if not TackemSystemAdmin().get_config(['api', 'enabled'], True):
            return False
        if TackemSystemAdmin().get_config(['webui', 'disabled'], False):
            return False
        if self.__webserver is not None:
            self.__webserver.start()
        return True

    def __stop_webserver(self):
        '''stops the Webserver'''
        if not TackemSystemAdmin().get_config(['api', 'enabled'], True):
            return False
        if TackemSystemAdmin().get_config(['webui', 'disabled'], False):
            return False
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
