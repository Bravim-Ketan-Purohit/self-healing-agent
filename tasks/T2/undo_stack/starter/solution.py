class TextEditor:
    """Text editor with insert, delete, undo, and redo support."""

    def __init__(self):
        pass

    @property
    def content(self) -> str:
        pass

    def insert(self, position: int, text: str) -> None:
        pass

    def delete(self, position: int, length: int) -> None:
        pass

    def undo(self) -> None:
        pass

    def redo(self) -> None:
        pass
