class ObservableList:
    """List wrapper that notifies callbacks on insert, remove, and set."""

    def __init__(self, initial: list = None):
        pass

    def subscribe(self, callback: callable) -> None:
        pass

    def unsubscribe(self, callback: callable) -> None:
        pass

    def insert(self, index: int, item) -> None:
        pass

    def remove(self, index: int) -> None:
        pass

    def set(self, index: int, item) -> None:
        pass

    def get(self, index: int):
        pass

    def __len__(self) -> int:
        pass

    def to_list(self) -> list:
        pass
