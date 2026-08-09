from solution import Trie
import pytest


def test_insert_and_search():
    t = Trie()
    t.insert("hello")
    assert t.search("hello") is True
    assert t.search("hell") is False


def test_starts_with():
    t = Trie()
    t.insert("cat")
    t.insert("car")
    t.insert("card")
    assert t.starts_with("ca") == ["car", "card", "cat"]


def test_delete_basic():
    t = Trie()
    t.insert("abc")
    t.delete("abc")
    assert t.search("abc") is False
    assert len(t) == 0


def test_delete_nonexistent_raises():
    t = Trie()
    t.insert("hello")
    with pytest.raises(KeyError):
        t.delete("world")
