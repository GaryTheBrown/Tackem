'''Start Point Of Program'''
# https://docs.cherrypy.org/en/latest/tutorials.html
import os
import os.path
import platform
import signal
from typing import Union
from data.config import CONFIG
from system.admin import TackemSystemAdmin
from data import PROGRAMCONFIGLOCATION
from libs.root_event import RootEventMaster as RootEvent


from libs.authenticator import Authentication
from libs.database import Database
from libs.webserver import Webserver
# TODO intergrate Libraries into main program
# is it going to be a single or multi instance?

# TODO allow the converter to be called from elsewhere in the system but keep its config in the
# Ripper section as this will mainly be for ripping but the user may want to convert a unsupported

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

    @classmethod
    def start(cls):
        '''Start of the program'''
        print("LOADING PLUGINS...")
        TackemSystemAdmin().load_plugins()
        print("LOADING Config...")
        CONFIG.load()
        print("LOADING DATABASE...")
        Database.setup_db()
        print("STARTING DATABASE...")
        Database.start_sql()
        print("STARTING AUTHENTICATOR...")
        Authentication.start()
        print("STARTING LIBRARIES...")
        print("TODO")
        #if (Ripper):
        #   print("STARTING RIPPER...")
        print("LOADING SYSTEMS...")
        TackemSystemAdmin().load_systems()
        print("STARTING SYSTEMS...")
        TackemSystemAdmin().start_systems()
        print("LOADING WEBSERVICES...")
        Webserver.load()
        print("STARTING WEBSERVICES...")
        Webserver.start()
        print("TACKEM HAS STARTED")

    @classmethod
    def stop(cls):
        '''Stop commands'''
        print("STOPPING WEB SERVICES...")
        Webserver.stop()
        print("STOPPING SYSTEMS...")
        TackemSystemAdmin().stop_systems()
        #if (Ripper):
        #   print("STARTING RIPPER...")
        print("STOPPING LIBRARIES...")
        print("TODO")
        print("STOPPING DATABASE...")
        Database.stop_sql()

    @classmethod
    def cleanup(cls):
        '''Cleanup commands'''
        print("CLEANING UP...")
        Webserver.delete()
        TackemSystemAdmin().unload_systems()
        TackemSystemAdmin().unload_plugins()

    @classmethod
    def shutdown(cls):
        '''Shutdown commands'''
        cls.stop()
        print("SAVING Config FILE...")
        CONFIG.save()
        print("SHUTDOWN COMPLETED")

    @classmethod
    def run(cls):
        '''Looping function'''

        if not os.path.exists(PROGRAMCONFIGLOCATION):
            os.mkdir(PROGRAMCONFIGLOCATION)

        signal.signal(signal.SIGINT, ctrl_c) # Setup signal to watch for ctrl + c command
        cls.start()
        while True:
            event, data = RootEvent.wait_and_get_event()

            if event is False:
                continue
            if event == "shutdown":
                cls.shutdown()
                break
            if event == "reboot":
                cls.shutdown()
                cls.start()
                continue
            if event == "start_system":
                TackemSystemAdmin().load_system(data, len(data.split(" ")) == 2)
                TackemSystemAdmin().start_system(data)
                Webserver.restart()
                continue
            if event == "stop_system":
                TackemSystemAdmin().stop_system(data)
                TackemSystemAdmin().unload_system(data)
                Webserver.restart()
                continue

            print("Event Not Recognised Ignoring")
            continue

        cls.cleanup()

# Catching the ctrl + c event and doing a clean shutdown
def ctrl_c(_, __):
    '''Function to call once ctrl + c is pressed'''
    print(" caught Shutting Down Cleanly...")
    RootEvent.set_event("shutdown")

if __name__ == "__main__":
    if platform.system() != 'Linux':
        print("""
This Program is only developed to run on LINUX Parts may not work as expected please report any
 issues you find for other platforms on guthub"""
        )
    Tackem().run()
    signal.signal(signal.SIGINT, False)
