"""Event to control the loop function"""
from typing import Optional
from threading import Event


class RootEvent:
    """Event to control the loop function"""

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


class RootEventMaster(RootEvent):
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
