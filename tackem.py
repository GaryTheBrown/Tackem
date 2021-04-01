"""Start Point Of Program"""
import platform
import signal

from data.config import CONFIG
from libs.authentication import Authentication
from libs.database import Database
from libs.events import RootEventMaster as RootEvent
from libs.ripper import Ripper
from www import Webserver

# TODO finish off the Ripper system
# TODO intergrate Libraries into main program
# TODO NEED A TOOL FOR AUDIO ISO TO {MUSIC FILE}
# TODO UNIT TEST WHOLE SYSTEM, SELENIUM ON THE PAGES TOO.
# TODO SETUP GITHUB ACTIONS TO DO ALL THIS TESTING
# TODO LOOK INTO TEMPLATING SYSTEM FOR HTML
# https://stackoverflow.com/questions/3435972/mako-or-jinja2
# https://pythonhosted.org/wheezy.template/index.html
# https://stackoverflow.com/questions/16844182/getting-started-with-cherrypy-and-jinja2
# https://stackoverflow.com/questions/5824881/python-call-special-method-practical-example


class Tackem:
    """main program entrance"""

    @classmethod
    def start(cls):
        """Start of the program"""
        print("LOADING Config...")
        CONFIG.load()
        print("STARTING DATABASE...")
        Database.start()
        print("STARTING authentication...")
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
        """Stop commands"""
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
        """Shutdown commands"""
        cls.stop()
        print("SAVING Config FILE...")
        CONFIG.save()
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
