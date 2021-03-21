"""Event to pass mesages to the ripper master from inside"""
from threading import Event
from typing import Optional

# TODO sort this and add in use in the main ripper init to allow passing data from inside subsystems


class RipperEvent:
    """Event to pass mesages to the ripper master from inside"""

    _events = []
    _event = Event()

    @classmethod
    def set_event(cls, event: str, data: Optional[str] = None, call: bool = True):
        """Set an event for the root thread to do"""
        cls._events.append((event, data))
        if call:
            cls._event.set()

    @classmethod
    def add_event(cls, event: str, data: Optional[str] = None):
        """Set an event for the root thread to do"""
        cls._events.append((event, data))

    @classmethod
    def call_event(cls):
        """Set an event for the root thread to do"""
        cls._event.set()


class RipperEventMaster(RipperEvent):
    """Event to wait for the command and then return what to do."""

    @classmethod
    def wait_and_get_event(cls) -> str:
        """waits for an event and returns it to root thread cleaning the event if needed"""
        if not cls._events:
            cls._event.wait()
        event = cls._events.pop()
        if not cls._events:
            cls._event.clear()
        return event
