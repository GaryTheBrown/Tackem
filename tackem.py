'''Start Point Of Program'''
# https://docs.cherrypy.org/en/latest/tutorials.html
from data import PROGRAMCONFIGLOCATION
import os
import os.path
import platform
import signal

from libs.root_event import RootEventMaster as RootEvent

from data.config import CONFIG
from libs.authenticator import Authentication
from libs.database import Database
from libs.webserver import Webserver
from libs.ripper import Ripper
# TODO intergrate Libraries into main program
# is it going to be a single or multi instance?

# TODO allow the converter to be called from elsewhere in the system but keep its config in the
# Ripper section as this will mainly be for ripping but the user may want to convert a unsupported

# TODO NEED A TOOL FOR AUDIO ISO TO {MUSIC FILE}

# TODO UNIT TEST WHOLE SYSTEM, SELENIUM ON THE PAGES TOO.
# TODO SETUP GITHUB ACTIONS TO DO ALL THIS TESTING
# TODO the same for all plugins

class Tackem:
    '''main program entrance'''

    @classmethod
    def start(cls):
        '''Start of the program'''
        print("LOADING Config...")
        CONFIG.load()
        print("STARTING DATABASE...")
        Database.start()
        print("STARTING AUTHENTICATOR...")
        Authentication.start()
        print("STARTING LIBRARIES... TODO")
        if Ripper.enabled:
            print("STARTING RIPPER...")
            Ripper.start()
        print("STARTING WEBSERVICES...")
        Webserver.start()
        print("TACKEM HAS STARTED")

    @classmethod
    def stop(cls):
        '''Stop commands'''
        print("STOPPING WEB SERVICES...")
        Webserver.stop()
        if Ripper.running:
           print("STOPPING RIPPER...")
           Ripper.stop()
        print("STOPPING LIBRARIES... TODO")
        print("STOPPING DATABASE...")
        Database.stop()

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

            print("Event Not Recognised Ignoring")
            continue


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
