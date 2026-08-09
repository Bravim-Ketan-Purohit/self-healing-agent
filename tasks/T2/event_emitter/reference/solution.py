from typing import Callable


class EventEmitter:
    """Publish/subscribe event system with on, off, once, and emit."""

    def __init__(self):
        self._listeners = {}  # event -> list of (callback, once_flag)

    def on(self, event: str, callback: Callable) -> None:
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append((callback, False))

    def off(self, event: str, callback: Callable) -> None:
        if event not in self._listeners:
            return
        listeners = self._listeners[event]
        # Remove first matching registration
        for i, (cb, _) in enumerate(listeners):
            if cb is callback:
                listeners.pop(i)
                return

    def once(self, event: str, callback: Callable) -> None:
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append((callback, True))

    def emit(self, event: str, *args, **kwargs) -> None:
        if event not in self._listeners:
            return
        # Snapshot the current listeners so removals during emit don't affect this call
        listeners_snapshot = list(self._listeners[event])
        to_remove = []
        for cb, is_once in listeners_snapshot:
            cb(*args, **kwargs)
            if is_once:
                to_remove.append((cb, is_once))
        # Remove once listeners after emission
        for item in to_remove:
            try:
                self._listeners[event].remove(item)
            except ValueError:
                pass
