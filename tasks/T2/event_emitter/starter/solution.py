from typing import Callable


class EventEmitter:
    """Publish/subscribe event system with on, off, once, and emit."""

    def __init__(self):
        pass

    def on(self, event: str, callback: Callable) -> None:
        pass

    def off(self, event: str, callback: Callable) -> None:
        pass

    def once(self, event: str, callback: Callable) -> None:
        pass

    def emit(self, event: str, *args, **kwargs) -> None:
        pass
