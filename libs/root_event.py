'''Event to control the loop function'''
from threading import Event

class RootEvent:
    '''Event to control the loop function'''
    _event_type = False
    _event_variable = False
    _event = Event()

    def set_event(self, event_type, event_variable=False):
        '''Set an event for the root thread to do'''
        if RootEvent._event_type is False:
            RootEvent._event_type = event_type
            RootEvent._event_variable = event_variable
            RootEvent._event.set()
            return True
        else:
            return False

class RootEventMaster(RootEvent):
    '''Event to wait for the command and then return what to do.'''
    def wait_and_get_event(self):
        '''waits for an event and returns it to root thread cleaning the event if needed'''
        RootEvent._event.wait()
        event_type = RootEvent._event_type
        event_variable = RootEvent._event_variable
        RootEvent._event_type = False
        RootEvent._event_variable = False
        RootEvent._event.clear()
        return event_type, event_variable
