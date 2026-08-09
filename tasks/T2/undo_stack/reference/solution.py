class TextEditor:
    """Text editor with insert, delete, undo, and redo support."""

    def __init__(self):
        self._content = ""
        self._undo_stack = []
        self._redo_stack = []

    @property
    def content(self) -> str:
        return self._content

    def insert(self, position: int, text: str) -> None:
        if position < 0 or position > len(self._content):
            raise IndexError("Insert position out of range")
        self._undo_stack.append(("insert", position, text))
        self._redo_stack.clear()
        self._content = self._content[:position] + text + self._content[position:]

    def delete(self, position: int, length: int) -> None:
        if length <= 0:
            raise ValueError("Delete length must be positive")
        if position < 0 or position + length > len(self._content):
            raise IndexError("Delete range out of bounds")
        deleted = self._content[position:position + length]
        self._undo_stack.append(("delete", position, deleted))
        self._redo_stack.clear()
        self._content = self._content[:position] + self._content[position + length:]

    def undo(self) -> None:
        if not self._undo_stack:
            raise IndexError("Nothing to undo")
        action, position, text = self._undo_stack.pop()
        if action == "insert":
            # Reverse an insert: delete the inserted text
            self._content = self._content[:position] + self._content[position + len(text):]
        elif action == "delete":
            # Reverse a delete: re-insert the deleted text
            self._content = self._content[:position] + text + self._content[position:]
        self._redo_stack.append((action, position, text))

    def redo(self) -> None:
        if not self._redo_stack:
            raise IndexError("Nothing to redo")
        action, position, text = self._redo_stack.pop()
        if action == "insert":
            self._content = self._content[:position] + text + self._content[position:]
        elif action == "delete":
            self._content = self._content[:position] + self._content[position + len(text):]
        self._undo_stack.append((action, position, text))
