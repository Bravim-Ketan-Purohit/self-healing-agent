class ObservableList:
    """List wrapper that notifies callbacks on insert, remove, and set."""

    def __init__(self, initial: list = None):
        self._data = list(initial) if initial else []
        self._callbacks = []

    def subscribe(self, callback: callable) -> None:
        self._callbacks.append(callback)

    def unsubscribe(self, callback: callable) -> None:
        try:
            self._callbacks.remove(callback)
        except ValueError:
            raise ValueError("Callback not registered")

    def insert(self, index: int, item) -> None:
        # Clamp index to valid insert range
        if index < 0:
            index = max(0, len(self._data) + index + 1)
        if index > len(self._data):
            index = len(self._data)
        self._data.insert(index, item)
        self._notify(("insert", index, item))

    def remove(self, index: int) -> None:
        if index < 0 or index >= len(self._data):
            raise IndexError("Index out of range")
        removed = self._data.pop(index)
        self._notify(("remove", index, removed))

    def set(self, index: int, item) -> None:
        if index < 0 or index >= len(self._data):
            raise IndexError("Index out of range")
        self._data[index] = item
        self._notify(("set", index, item))

    def get(self, index: int):
        if index < 0 or index >= len(self._data):
            raise IndexError("Index out of range")
        return self._data[index]

    def __len__(self) -> int:
        return len(self._data)

    def to_list(self) -> list:
        return list(self._data)

    def _notify(self, event: tuple) -> None:
        for cb in self._callbacks:
            cb(event)
