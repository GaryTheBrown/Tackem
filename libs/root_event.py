'''Event to control the loop function'''
from threading import Event


class RootEvent:
    '''Event to control the loop function'''
    _event_type = False
    _event = Event()

    @classmethod
    def set_event(cls, event_type: str) -> bool:
        '''Set an event for the root thread to do'''
        if cls._event_type is False:
            cls._event_type = event_type
            cls._event.set()
            return True
        return False


class RootEventMaster(RootEvent):
    '''Event to wait for the command and then return what to do.'''

    @classmethod
    def wait_and_get_event(cls) -> str:
        '''waits for an event and returns it to root thread cleaning the event if needed'''
        cls._event.wait()
        event_type = cls._event_type
        cls._event_type = False
        cls._event.clear()
        return event_type
