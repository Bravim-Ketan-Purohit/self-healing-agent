from solution import TextEditor
import pytest


def test_redo_cleared_on_new_edit():
    """Invariant: redo stack is cleared when a new edit is performed after undo."""
    editor = TextEditor()
    editor.insert(0, "abc")
    editor.insert(3, "def")
    editor.undo()
    editor.insert(3, "xyz")
    with pytest.raises(IndexError):
        editor.redo()


def test_multiple_undo_redo_consistency():
    """Invariant: multiple undo/redo cycles maintain content consistency."""
    editor = TextEditor()
    editor.insert(0, "a")
    editor.insert(1, "b")
    editor.insert(2, "c")
    assert editor.content == "abc"
    editor.undo()
    assert editor.content == "ab"
    editor.undo()
    assert editor.content == "a"
    editor.redo()
    assert editor.content == "ab"
    editor.redo()
    assert editor.content == "abc"


def test_undo_delete_restores_text():
    """Invariant: undoing a delete restores the exact deleted text at correct position."""
    editor = TextEditor()
    editor.insert(0, "hello world")
    editor.delete(5, 6)
    assert editor.content == "hello"
    editor.undo()
    assert editor.content == "hello world"


def test_undo_empty_raises():
    """Invariant: undo on empty history raises IndexError."""
    editor = TextEditor()
    with pytest.raises(IndexError):
        editor.undo()


def test_redo_empty_raises():
    """Invariant: redo with nothing to redo raises IndexError."""
    editor = TextEditor()
    editor.insert(0, "x")
    with pytest.raises(IndexError):
        editor.redo()


def test_interleaved_operations():
    """Invariant: content is always consistent with applied operations."""
    editor = TextEditor()
    editor.insert(0, "ABCDE")
    editor.delete(1, 2)  # "ADE"
    editor.insert(1, "xyz")  # "AxyzDE"
    assert editor.content == "AxyzDE"
    editor.undo()
    assert editor.content == "ADE"
    editor.undo()
    assert editor.content == "ABCDE"
    editor.redo()
    assert editor.content == "ADE"


def test_insert_out_of_range_raises():
    """Invariant: insert at invalid position raises IndexError."""
    editor = TextEditor()
    editor.insert(0, "hi")
    with pytest.raises(IndexError):
        editor.insert(10, "x")


def test_delete_invalid_range_raises():
    """Invariant: delete with invalid range raises appropriate error."""
    editor = TextEditor()
    editor.insert(0, "abc")
    with pytest.raises(IndexError):
        editor.delete(2, 5)  # exceeds content
    with pytest.raises(ValueError):
        editor.delete(0, 0)  # length <= 0
    with pytest.raises(ValueError):
        editor.delete(0, -1)
