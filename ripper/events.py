"""Event to pass mesages to the ripper master from inside"""
from threading import Event
from typing import Any
from typing import Tuple


class RipperEvent:
    """Event to pass mesages to the ripper master from inside"""

    _events = []
    _event = Event()

    @classmethod
    def do(cls, event: str, *data):
        """Set an event for the ripper system to do"""
        cls._events.append((event, data))
        cls._event.set()


class RipperEventMaster(RipperEvent):
    """Event to wait for the command and then return what to do."""

    __running = True

    @classmethod
    def wait_and_get_event(cls) -> Tuple[str, Tuple[Any]]:
        """waits for an event and returns it to ripper system cleaning the event if needed"""
        if not cls._events:
            cls._event.wait()
        if not cls.__running:
            return
        event = cls._events.pop()
        if not cls._events:
            cls._event.clear()
        return event

    @classmethod
    def stop(cls):
        """Kills the system"""
        cls.__running = False
        cls._event.set()
