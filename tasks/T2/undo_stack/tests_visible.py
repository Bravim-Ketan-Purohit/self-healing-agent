from solution import TextEditor
import pytest


def test_insert_and_content():
    editor = TextEditor()
    editor.insert(0, "hello")
    editor.insert(5, " world")
    assert editor.content == "hello world"


def test_delete():
    editor = TextEditor()
    editor.insert(0, "abcdef")
    editor.delete(2, 3)
    assert editor.content == "abf"


def test_undo_insert():
    editor = TextEditor()
    editor.insert(0, "hello")
    editor.undo()
    assert editor.content == ""


def test_redo_after_undo():
    editor = TextEditor()
    editor.insert(0, "test")
    editor.undo()
    editor.redo()
    assert editor.content == "test"
