'''Event to control the loop function'''
from threading import Event
from time import sleep
class RootEvent:
    '''Event to control the loop function'''
    _shutdown = False
    _reboot = False
    _wait_time = 0
    _event = Event()

    def shutdown(self, wait_time=0):
        '''Shutdown command'''
        if not RootEvent._reboot and not RootEvent._shutdown:
            RootEvent._shutdown = True
            RootEvent._wait_time = wait_time
            RootEvent._event.set()

    def reboot(self, wait_time=0):
        '''reboot command'''
        if not RootEvent._reboot and not RootEvent._shutdown:
            RootEvent._reboot = True
            RootEvent._wait_time = wait_time
            RootEvent._event.set()

class RootEventMaster(RootEvent):
    '''Event to wait for the command and then return what to do.'''
    def wait(self):
        '''function to wait for the event'''
        RootEvent._event.wait()
        if RootEvent._wait_time > 0:
            print("waiting " + str(RootEvent._wait_time) + "seconds to shutdown")
            sleep(float(RootEvent._wait_time))

    def check_shutdown(self):
        '''returns if the command is shutdown'''
        return RootEvent._shutdown

    def check_reboot(self):
        '''returns if the command is reboot'''
        return RootEvent._reboot

    def clear_event(self):
        '''Reset the Event if set to reboot'''
        if RootEvent._reboot and not RootEvent._shutdown:
            RootEvent._reboot = False
            RootEvent._event.clear()
