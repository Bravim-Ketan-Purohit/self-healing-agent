# Undo Stack

Implement a `TextEditor` class that models a simple text editor with undo/redo support:

- `__init__(self)` — Create an editor with empty text content.
- `insert(self, position: int, text: str) -> None` — Insert text at the given position. Raises `IndexError` if position is out of range [0, len(content)].
- `delete(self, position: int, length: int) -> None` — Delete `length` characters starting at position. Raises `IndexError` if the range is invalid. Raises `ValueError` if length <= 0.
- `undo(self) -> None` — Undo the last edit operation. Raises `IndexError` if nothing to undo.
- `redo(self) -> None` — Redo the last undone operation. Raises `IndexError` if nothing to redo.
- `content` — Property that returns the current text as a string.

## Invariants

- Performing a new edit (insert or delete) after an undo clears the redo stack.
- Undo followed by redo restores the exact previous state.
- The content is always consistent with the sequence of applied operations.

## Examples

```python
editor = TextEditor()
editor.insert(0, "hello")
editor.insert(5, " world")
editor.content  # "hello world"
editor.undo()
editor.content  # "hello"
editor.redo()
editor.content  # "hello world"
editor.undo()
editor.insert(5, "!")
editor.content  # "hello!"
editor.redo()   # raises IndexError (redo cleared by new edit)
```
