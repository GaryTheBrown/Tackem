"""Start Point Of Program"""
import platform
import signal

from config import CONFIG
from database import Database
from libraries import Library
from libs.auth import Auth
from libs.events import RootEventMaster as RootEvent
from libs.scraper import Scraper
from ripper import Ripper
from www import Webserver

# TODO intergrate Libraries into main program
# TODO finish off the Ripper system
# TODO NEED A TOOL FOR AUDIO ISO TO {MUSIC FILE}
# TODO UNIT TEST WHOLE SYSTEM, SELENIUM ON THE PAGES TOO.
# TODO SETUP GITHUB ACTIONS TO DO ALL THIS TESTING


class Tackem:
    """main program entrance"""

    @staticmethod
    def start():
        """Start of the program"""
        print("LOADING Config...", end=" ")
        CONFIG.load()
        print("DONE")
        print("SETTING UP DATABASE...", end=" ")
        Database.setup()
        print("DONE")
        print("LOADING AUTHENTICATION...", end=" ")
        Auth.start()
        print("DONE")
        print("LOADING SCRAPER...", end=" ")
        Scraper.start()
        print("DONE")
        print("LOADING LIBRARIES...", end=" ")
        Library.start()
        print("DONE")
        if Ripper.enabled:
            print("STARTING RIPPER...", end=" ")
            Ripper.start()
            print("DONE")
        print("STARTING WEBSERVICES...", end=" ")
        Webserver.start()
        print("DONE")
        print("TACKEM HAS STARTED")

    @staticmethod
    def shutdown():
        """Shutdown commands"""
        print("STOPPING WEB SERVICES...", end=" ")
        Webserver.stop()
        print("DONE")
        if Ripper.running:
            print("STOPPING RIPPER...", end=" ")
            Ripper.stop()
            print("DONE")
        print("STOPPING LIBRARIES...", end=" ")
        Library.stop()
        print("DONE")
        print("SAVING Config FILE...", end=" ")
        CONFIG.save()
        print("DONE")
        print("SHUTDOWN COMPLETED")

    @classmethod
    def run(cls):
        """Looping function"""
        # Setup signal to watch for ctrl + c command
        signal.signal(signal.SIGINT, ctrl_c)
        cls.start()
        while True:
            event, data = RootEvent.wait_and_get_event()

            if event is False:
                continue
            if event == "shutdown":
                cls.shutdown()
                exit()
            if event == "reboot":
                cls.shutdown()
                cls.start()
                continue

            print("Event Not Recognised Ignoring")
            continue


# Catching the ctrl + c event and doing a clean shutdown
def ctrl_c(_, __):
    """Function to call once ctrl + c is pressed"""
    print(" caught Shutting Down Cleanly...")
    RootEvent.set_event("shutdown")


if __name__ == "__main__":
    if platform.system() != "Linux":
        print(
            """
This Program is only developed to run on LINUX Parts may not work as expected please report any
 issues you find for other platforms on guthub"""
        )
    Tackem().run()
    signal.signal(signal.SIGINT, False)
