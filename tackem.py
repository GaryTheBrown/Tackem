"""Start Point Of Program"""
import platform
import signal

from data.config import CONFIG
from libs.authentication import Authentication
from libs.database import Database
from libs.events import RootEventMaster as RootEvent
from libs.ripper import Ripper
from libs.scraper import Scraper
from www import Webserver

# TODO finish off the Ripper system
# TODO intergrate Libraries into main program
# TODO NEED A TOOL FOR AUDIO ISO TO {MUSIC FILE}
# TODO UNIT TEST WHOLE SYSTEM, SELENIUM ON THE PAGES TOO.
# TODO SETUP GITHUB ACTIONS TO DO ALL THIS TESTING


class Tackem:
    """main program entrance"""

    @classmethod
    def start(cls):
        """Start of the program"""
        print("LOADING Config...", end=" ")
        CONFIG.load()
        print("DONE")
        print("STARTING DATABASE...", end=" ")
        Database.start()
        print("DONE")
        print("STARTING AUTHENTICATION...", end=" ")
        Authentication.start()
        print("DONE")
        print("STARTING SCRAPER...", end=" ")
        Scraper.start()
        print("DONE")
        print("STARTING LIBRARIES...", end=" ")
        print("TODO")
        if Ripper.enabled:
            print("STARTING RIPPER...", end=" ")
            Ripper.start()
            print("DONE")
        print("STARTING WEBSERVICES...", end=" ")
        Webserver.start()
        print("DONE")
        print("TACKEM HAS STARTED")

    @classmethod
    def stop(cls):
        """Stop commands"""
        print("STOPPING WEB SERVICES...", end=" ")
        Webserver.stop()
        print("DONE")
        if Ripper.running:
            print("STOPPING RIPPER...", end=" ")
            Ripper.stop()
            print("DONE")
        print("STOPPING LIBRARIES...", end=" ")
        print("TODO")
        print("STOPPING DATABASE...", end=" ")
        Database.stop()
        print("DONE")

    @classmethod
    def shutdown(cls):
        """Shutdown commands"""
        cls.stop()
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
