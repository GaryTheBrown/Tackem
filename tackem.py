'''Start Point Of Program'''
#https://docs.cherrypy.org/en/latest/tutorials.html
import os
import os.path
import signal
from libs.startup_arguments import ARGS
from libs.root_event import RootEventMaster as RootEvent
from system.admin import TackemSystemAdmin

class Tackem:
    '''main program entrance'''
    def __init__(self):
        pass

    def load(self):
        '''Load of the program'''
        print("LOADING PLUGINS...")
        TackemSystemAdmin().load_plugins()
        print("LOADING CONFIG...")
        TackemSystemAdmin().load_plugin_cfgs()
        TackemSystemAdmin().load_config()

        if not TackemSystemAdmin().get_config(['firstrun'], True):
            print("LOADING DATABASE...")
            TackemSystemAdmin().load_sql()
            print("LOADING MUSICBRAINZ...")
            TackemSystemAdmin().load_musicbrainz()
            print("LOADING AUTHENTICATOR...")
            TackemSystemAdmin().load_auth()
            print("LOADING SYSTEMS...")
            TackemSystemAdmin().load_systems()

        print("LOADING WEBSERVICES...")
        TackemSystemAdmin().load_webserver()

    def start(self):
        '''Startup Of the systems'''
        if not TackemSystemAdmin().get_config(['firstrun'], True):
            print("STARTING DATABASE...")
            TackemSystemAdmin().start_sql()
            print("STARTING AUTHENTICATOR...")
            TackemSystemAdmin().start_auth()
            print("STARTING SYSTEMS...")
            TackemSystemAdmin().start_systems()
        print("STARTING WEBSERVICES...")
        TackemSystemAdmin().start_webserver()
        print("TACKEM HAS STARTED")

    def stop(self):
        '''Stop commands'''
        print("STOPPING WEB SERVICES...")
        TackemSystemAdmin().stop_webserver()
        if not TackemSystemAdmin().get_config(['firstrun'], True):
            print("STOPPING SYSTEMS...")
            TackemSystemAdmin().stop_systems()
            print("STOPPING DATABASE...")
            TackemSystemAdmin().stop_sql()

    def cleanup(self):
        '''Cleanup commands'''
        print("CLEANING UP...")
        TackemSystemAdmin().delete_webserver()
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

        self.load()
        self.start()
        while True:
            event_type, event_variable = RootEvent().wait_and_get_event()

            if event_type is False:
                continue
            elif event_type == "shutdown":
                self.shutdown()
                break
            elif event_type == "reboot":
                self.shutdown()
                self.load()
                self.start()
            # elif event_type == "start system":
            #     if event_variable is False:
            #         continue
            #     self.system_start(event_variable)
            # elif event_type == "stop system":
            #     if event_variable is False:
            #         continue
            #     self.system_stop(event_variable)
            # elif event_type == "restart system":
            #     if event_variable is False:
            #         continue
            #     self.system_stop(event_variable)
            #     self.system_start(event_variable)
            else:
                print("Event Not Recognised Ignoring")
                continue

        self.cleanup()

##############################################
# Catching the ctrl + c event and doing a clean shutdown
def ctrl_c(_, __):
    '''Function to call once ctrl + c is pressed'''
    print(" caught Shutting Down Cleanly...")
    RootEvent().set_event("shutdown")
##############################################

if __name__ == "__main__":
    Tackem().run()
    signal.signal(signal.SIGINT, False)
